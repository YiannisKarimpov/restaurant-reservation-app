"""
Main routes for the application.
Handles home, restaurant info, menu, and reservation pages.
"""
from flask import request, redirect, flash, url_for, Blueprint, render_template
from flask_login import current_user
from app.models import Reservation, Restaurant, MenuItem
from app import db


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html')


@main_bp.route('/menu')
def menu():
    """Menu display route."""
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
    
    # Check if menu items exist, if not create them
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    if len(menu_items) == 0:
        print("DEBUG: Creating menu items...")
        items = [
            MenuItem(restaurant_id=restaurant.id, name='Caesar Salad', description='Fresh romaine with parmesan', price=12.99, category='Appetizer'),
            MenuItem(restaurant_id=restaurant.id, name='Grilled Salmon', description='Atlantic salmon with lemon butter', price=24.99, category='Main'),
            MenuItem(restaurant_id=restaurant.id, name='Ribeye Steak', description='Prime ribeye with garlic mash', price=32.99, category='Main'),
            MenuItem(restaurant_id=restaurant.id, name='Pasta Carbonara', description='Classic Italian pasta', price=18.99, category='Main'),
            MenuItem(restaurant_id=restaurant.id, name='Chocolate Cake', description='Decadent dark chocolate', price=9.99, category='Dessert'),
            MenuItem(restaurant_id=restaurant.id, name='House Wine', description='Local red wine', price=7.99, category='Beverage'),
        ]
        db.session.add_all(items)
        db.session.commit()
        print(f"DEBUG: Created {len(items)} menu items")
    
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


@main_bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    """Reservation page route."""
    from flask_login import login_required
    from datetime import datetime, timedelta
    
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please log in to make a reservation!', 'error')
            return redirect(url_for('auth.login'))
        
        restaurant_id = request.form.get('restaurant_id')
        reservation_date = request.form.get('reservation_date')
        reservation_time = request.form.get('reservation_time')
        party_size = request.form.get('party_size')
        special_requests = request.form.get('special_requests')
        
        if not all([restaurant_id, reservation_date, reservation_time, party_size]):
            flash('All fields are required!', 'error')
            return redirect(url_for('main.reserve'))
        
        reservation = Reservation(
            user_id=current_user.id,
            restaurant_id=int(restaurant_id),
            reservation_date=datetime.strptime(reservation_date, '%Y-%m-%d').date(),
            reservation_time=datetime.strptime(reservation_time, '%H:%M').time(),
            party_size=int(party_size),
            special_requests=special_requests
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        flash('Reservation confirmed! Check your dashboard.', 'success')
        return redirect(url_for('dashboard.index'))
    
    restaurant = Restaurant.query.first()
    return render_template('reserve.html', restaurant=restaurant)


@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    """Contact page route."""
    return render_template('contact.html')
