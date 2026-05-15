"""
Main routes for the application.
Handles home, restaurant info, menu, and reservation pages.
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html')


@main_bp.route('/menu')
def menu():
    """Menu display route."""
    return render_template('menu.html')


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
