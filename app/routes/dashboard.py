"""
Dashboard routes for user profile and reservation management.
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Reservation

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


@dashboard_bp.route('/reservations/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_reservation(id):
    """Cancel a reservation."""
    from app.models import Reservation
    
    reservation = Reservation.query.get_or_404(id)
    
    # Check if user owns this reservation
    if reservation.user_id != current_user.id:
        flash('You can only cancel your own reservations!', 'error')
        return redirect(url_for('dashboard.reservations'))
    
    # Check if already cancelled
    if reservation.status == 'cancelled':
        flash('This reservation is already cancelled!', 'error')
        return redirect(url_for('dashboard.reservations'))
    
    reservation.status = 'cancelled'
    db.session.commit()
    
    flash('Reservation cancelled successfully!', 'success')
    return redirect(url_for('dashboard.reservations'))


@dashboard_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('dashboard/profile.html', user=current_user)