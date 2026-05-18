"""
Dashboard routes for user profile and reservation management.
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    """User dashboard home."""
    return render_template('dashboard/index.html', user=current_user)


@dashboard_bp.route('/reservations')
@login_required
def reservations():
    """View user reservations."""
    user_reservations = current_user.reservations
    return render_template('dashboard/reservations.html', reservations=user_reservations)


@dashboard_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('dashboard/profile.html', user=current_user)