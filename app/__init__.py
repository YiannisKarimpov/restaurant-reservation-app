"""
Application factory for Restaurant Reservation App.
Initializes Flask app, database, and authentication.
"""
from flask import render_template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='development'):
    """
    Application factory function.
    
    Args:
        config_name (str): Configuration environment ('development', 'production', 'testing')
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from database by ID."""
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Add is_admin column if it doesn't exist (migration fallback)
        from sqlalchemy import text
        try:
            db.session.execute(text('ALTER TABLE "user" ADD COLUMN is_admin BOOLEAN DEFAULT FALSE'))
            db.session.commit()
            print("Added is_admin column")
        except Exception:
            db.session.rollback()
        # Grant admin to the admin user
        try:
            from app.models import User
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user and not admin_user.is_admin:
                admin_user.is_admin = True
                db.session.commit()
                print("Admin user granted admin access")
        except Exception:
            db.session.rollback()
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Database tables: {tables}")

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app
