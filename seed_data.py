"""
Seed Render's database with sample data.
"""
import os
from app import create_app, db
from app.models import Restaurant, Special
from datetime import datetime, timedelta

# Use production config to connect to Render's DB
os.environ['FLASK_ENV'] = 'production'
os.environ['DB_HOST'] = 'dpg-d8h8ummk1jcs739m7sqg-a'  # From Render dashboard
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = 'restaurant_db_0saa'
os.environ['DB_USER'] = 'restaurant_db_0saa_user'
os.environ['DB_PASSWORD'] = '6GaUliLoOtYQAHPa8KZKoJLgViM3Flzf'  # From Render dashboard

app = create_app('production')

with app.app_context():
    restaurant = Restaurant.query.first()
    if not restaurant:
        restaurant = Restaurant(
            name='Bistro Restaurant',
            description='Fine dining experience',
            address='123 Main Street',
            phone='555-0100',
            email='info@bistro.com',
            opening_hours='11:00 AM - 10:00 PM'
        )
        db.session.add(restaurant)
        db.session.commit()
    
    # Delete old specials
    Special.query.delete()
    db.session.commit()
    
    # Add sample specials
    specials = [
        Special(
            restaurant_id=restaurant.id,
            title='Summer Special',
            description='Enjoy 20% off on all appetizers this summer!',
            discount='20% Off Appetizers',
            valid_until=datetime(2026, 12, 31).date()
        ),
        Special(
            restaurant_id=restaurant.id,
            title='Happy Hour',
            description='Get $5 off any main course between 4-6 PM',
            discount='$5 Off Main',
            valid_until=datetime(2026, 12, 31).date()
        ),
        Special(
            restaurant_id=restaurant.id,
            title='Weekend Brunch',
            description='Join us for our special weekend brunch menu',
            discount='Brunch Special',
            valid_until=datetime(2026, 12, 31).date()
        ),
    ]
    
    db.session.add_all(specials)
    db.session.commit()
    print("✅ Sample specials added!")