"""
Admin routes for restaurant management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Reservation, Restaurant, MenuItem

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to check if user is authenticated and is an admin."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('Admin access required!', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard."""
    total_users = User.query.count()
    total_reservations = Reservation.query.count()
    total_menu_items = MenuItem.query.count()
    
    recent_reservations = Reservation.query.order_by(Reservation.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_reservations=total_reservations,
                         total_menu_items=total_menu_items,
                         recent_reservations=recent_reservations)


@admin_bp.route('/reservations')
@admin_required
def reservations():
    """View all reservations."""
    reservations = Reservation.query.order_by(Reservation.reservation_date.desc()).all()
    return render_template('admin/reservations.html', reservations=reservations)


@admin_bp.route('/reservations/<int:id>/confirm', methods=['POST'])
@admin_required
def confirm_reservation(id):
    """Confirm a reservation."""
    reservation = Reservation.query.get_or_404(id)
    reservation.status = 'confirmed'
    db.session.commit()
    flash('Reservation confirmed!', 'success')
    return redirect(url_for('admin.reservations'))


@admin_bp.route('/reservations/<int:id>/cancel', methods=['POST'])
@admin_required
def cancel_reservation(id):
    """Cancel a reservation."""
    reservation = Reservation.query.get_or_404(id)
    reservation.status = 'cancelled'
    db.session.commit()
    flash('Reservation cancelled!', 'success')
    return redirect(url_for('admin.reservations'))


@admin_bp.route('/menu')
@admin_required
def menu():
    """Manage menu items."""
    menu_items = MenuItem.query.all()
    return render_template('admin/menu.html', menu_items=menu_items)


@admin_bp.route('/menu/add', methods=['GET', 'POST'])
@admin_required
def add_menu_item():
    """Add new menu item."""
    if request.method == 'POST':
        restaurant = Restaurant.query.first()
        
        item = MenuItem(
            restaurant_id=restaurant.id,
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category')
        )
        
        db.session.add(item)
        db.session.commit()
        
        flash('Menu item added!', 'success')
        return redirect(url_for('admin.menu'))
    
    return render_template('admin/add_menu_item.html')


@admin_bp.route('/menu/<int:id>/delete', methods=['POST'])
@admin_required
def delete_menu_item(id):
    """Delete menu item."""
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item deleted!', 'success')
    return redirect(url_for('admin.menu'))


@admin_bp.route('/users')
@admin_required
def users():
    """View all users."""
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/specials')
@admin_required
def view_specials():
    """View all specials."""
    from app.models import Special
    specials = Special.query.all()
    return render_template('admin/specials.html', specials=specials)


@admin_bp.route('/specials/add', methods=['GET', 'POST'])
@admin_required
def add_special():
    """Add new special offer."""
    from app.models import Special, Restaurant
    from datetime import datetime
    
    if request.method == 'POST':
        restaurant = Restaurant.query.first()
        title = request.form.get('title')
        description = request.form.get('description')
        discount = request.form.get('discount')
        valid_until = request.form.get('valid_until')
        
        if not all([title, description, discount, valid_until]):
            flash('All fields required!', 'error')
            return redirect(url_for('admin.add_special'))
        
        special = Special(
            restaurant_id=restaurant.id,
            title=title,
            description=description,
            discount=discount,
            valid_until=datetime.strptime(valid_until, '%Y-%m-%d').date()
        )
        db.session.add(special)
        db.session.commit()
        
        flash('Special added!', 'success')
        return redirect(url_for('admin.view_specials'))
    
    return render_template('admin/add_special.html')


@admin_bp.route('/specials/<int:id>/delete', methods=['POST'])
@admin_required
def delete_special(id):
    """Delete a special offer."""
    from app.models import Special
    special = Special.query.get_or_404(id)
    db.session.delete(special)
    db.session.commit()
    flash('Special deleted!', 'success')
    return redirect(url_for('admin.view_specials'))