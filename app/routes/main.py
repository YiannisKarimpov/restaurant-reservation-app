"""
Main routes for the application.
Handles home, restaurant info, menu, and reservation pages.
"""
from app.models import Restaurant, MenuItem
from app import db

from flask import Blueprint, render_template

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


@main_bp.route('/reserve')
def reserve():
    """Reservation page route."""
    return render_template('reserve.html')


@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    """Contact page route."""
    return render_template('contact.html')
