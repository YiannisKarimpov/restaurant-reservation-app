"""
Main routes for the application.
Handles home, restaurant info, menu, and reservation pages.
"""
from sqlalchemy import or_
from flask import request, redirect, flash, url_for, Blueprint, render_template
from flask_login import current_user
from app.models import Reservation, Restaurant, MenuItem, Review, Special
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
    from datetime import datetime, timedelta
    
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please log in to make a reservation!', 'error')
            return redirect(url_for('auth.login'))
        
        try:
            restaurant_id = request.form.get('restaurant_id')
            reservation_date = request.form.get('reservation_date')
            reservation_time = request.form.get('reservation_time')
            party_size = request.form.get('party_size')
            special_requests = request.form.get('special_requests')
            
            if not all([restaurant_id, reservation_date, reservation_time, party_size]):
                flash('All fields are required!', 'error')
                return redirect(url_for('main.reserve'))
            
            # Validate party size
            try:
                party_size = int(party_size)
                if party_size < 1 or party_size > 20:
                    flash('Party size must be between 1 and 20!', 'error')
                    return redirect(url_for('main.reserve'))
            except ValueError:
                flash('Invalid party size!', 'error')
                return redirect(url_for('main.reserve'))
            
            # Validate date is in future
            res_date = datetime.strptime(reservation_date, '%Y-%m-%d').date()
            if res_date < datetime.now().date():
                flash('Reservation date must be in the future!', 'error')
                return redirect(url_for('main.reserve'))
            
            reservation = Reservation(
                user_id=current_user.id,
                restaurant_id=int(restaurant_id),
                reservation_date=res_date,
                reservation_time=datetime.strptime(reservation_time, '%H:%M').time(),
                party_size=party_size,
                special_requests=special_requests
            )
            
            db.session.add(reservation)
            db.session.commit()
            
            flash('Reservation confirmed! Check your dashboard.', 'success')
            return redirect(url_for('dashboard.index'))
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('main.reserve'))
    
    restaurant = Restaurant.query.first()
    today = datetime.now().date().isoformat()
    return render_template('reserve.html', restaurant=restaurant, today=today)


@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route."""
    from app.models import ContactMessage
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, subject, message]):
            flash('All fields are required!', 'error')
            return redirect(url_for('main.contact'))
        
        # Save to database
        contact_msg = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        db.session.add(contact_msg)
        db.session.commit()
        
        flash('Thank you! We received your message and will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html')


@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search menu items and reservations."""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'menu')
    results = []
    
    if query:
        if search_type == 'menu':
            results = MenuItem.query.filter(
                or_(
                    MenuItem.name.ilike(f'%{query}%'),
                    MenuItem.description.ilike(f'%{query}%'),
                    MenuItem.category.ilike(f'%{query}%')
                )
            ).all()
        elif search_type == 'category':
            results = MenuItem.query.filter_by(category=query).all()
    
    return render_template('search.html', results=results, query=query, search_type=search_type)


@main_bp.route('/menu/filter')
def filter_menu():
    """Filter menu by category."""
    category = request.args.get('category', '')
    restaurant = Restaurant.query.first()
    
    if category:
        menu_items = MenuItem.query.filter_by(
            restaurant_id=restaurant.id,
            category=category
        ).all()
    else:
        menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    
    categories = db.session.query(MenuItem.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('menu_filtered.html', 
                         menu_items=menu_items, 
                         categories=categories,
                         selected_category=category,
                         restaurant=restaurant)


@main_bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    """View and submit reviews."""
    from app.models import Review
    
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please log in to leave a review!', 'error')
            return redirect(url_for('auth.login'))
        
        restaurant = Restaurant.query.first()
        rating = request.form.get('rating')
        title = request.form.get('title')
        comment = request.form.get('comment')
        
        if not all([rating, title, comment]):
            flash('All fields are required!', 'error')
            return redirect(url_for('main.reviews'))
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                flash('Rating must be between 1 and 5!', 'error')
                return redirect(url_for('main.reviews'))
        except ValueError:
            flash('Invalid rating!', 'error')
            return redirect(url_for('main.reviews'))
        
        review = Review(
            user_id=current_user.id,
            restaurant_id=restaurant.id,
            rating=rating,
            title=title,
            comment=comment
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Thank you for your review!', 'success')
        return redirect(url_for('main.reviews'))
    
    restaurant = Restaurant.query.first()
    reviews = Review.query.filter_by(restaurant_id=restaurant.id).order_by(Review.created_at.desc()).all()
    return render_template('reviews.html', reviews=reviews, restaurant=restaurant)


@main_bp.route('/specials')
def specials():
    """View current specials and promotions."""
    try:
        restaurant = Restaurant.query.first()
        
        if not restaurant:
            specials_list = []
        else:
            from datetime import datetime
            specials_list = Special.query.filter_by(restaurant_id=restaurant.id).all()
            # Filter by valid_until >= today
            specials_list = [s for s in specials_list if s.valid_until >= datetime.now().date()]
        
        return render_template('specials.html', specials=specials_list, restaurant=restaurant)
    
    except Exception as e:
        flash('Error loading specials', 'error')
        return render_template('specials.html', specials=[], restaurant=None)
