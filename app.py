import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer
import secrets
import pymysql
from flask_wtf.csrf import CSRFProtect
from flask_limiter.errors import RateLimitExceeded
from wtforms import ValidationError

# Import extensions
from extensions import db, login_manager, bcrypt, limiter

# Load environment variables
load_dotenv()

# Initialize CSRF protection
csrf = CSRFProtect()

# MySQL connection
pymysql.install_as_MySQLdb()

# Create Flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

    # CSRF Protection
    csrf.init_app(app)

    # Database configuration

    # Construct the MySQL URL from individual environment variables if DATABASE_URL is not provided
    # Use defaults to avoid None values
    mysql_user = os.environ.get('MYSQL_USER', '')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_host = os.environ.get('MYSQL_HOST', '')  # Default to localhost if not set
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_database = os.environ.get('MYSQL_DATABASE', '')
    
    # Make sure all values are strings
    mysql_port = str(mysql_port)
    
    # Check if required parameters are set
    if not mysql_host or not mysql_user or not mysql_database:
        print(f"WARNING: Missing database configuration. Host: {mysql_host}, User: {mysql_user}, Database: {mysql_database}")
    
    db_uri = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
    print(f"Database URI: {db_uri}")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set secure cookie flags for session cookies
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Prevent CSRF via cross-site requests

    # Set session timeout (30 minutes of inactivity)
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 1800 seconds = 30 minutes

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    
    # Register custom error handler for rate limiting
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        # Check if it's an API request (expecting JSON)
        if request.path.startswith('/api/') or request.headers.get('Accept') == 'application/json':
            return jsonify({"error": "Rate limit exceeded", "message": str(e)}), 429
        # Otherwise, return the HTML template
        return render_template('rate_limit_error.html', message=str(e)), 429

    @app.errorhandler(400)
    def bad_request_error(error):
        flash('Bad request. Please check your input and try again.', 'warning')
        return render_template('400.html'), 400

    @app.errorhandler(403)
    def forbidden_error(error):
        flash('You do not have permission to access this resource.', 'warning')
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        flash('The page you are looking for was not found.', 'warning')
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        flash('An unexpected error occurred. Please try again later.', 'danger')
        return render_template('500.html'), 500

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    return app

# Create Flask app
app = create_app()

# Import models - must be after db initialization
from models import User, Transaction

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes after app creation
from routes import *

# Password policy validator
import re

def validate_password_strength(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character.')

# Database initialization function
def init_db():
    """Initialize the database with required tables and default admin user."""
    with app.app_context():
        db.create_all()
        # Check if there are admin users, if not create one
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@bankapp.com",
                account_number="0000000001",
                status="active",
                is_admin=True,
                balance=0.0
            )
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            print("Created admin user with username 'admin' and password 'admin123'")

# Enhance user notification messages for login, logout, transfer, password reset, registration, and errors
# (Implementation is in routes.py, but here is a reminder to ensure all critical actions use clear flash messages)
# Example usage in routes.py:
# flash('Login successful! Welcome back.', 'success')
# flash('You have been logged out.', 'info')
# flash('Transfer completed successfully.', 'success')
# flash('Password reset email sent. Please check your inbox.', 'info')
# flash('Registration successful! Please wait for admin approval.', 'success')
# flash('An error occurred. Please try again.', 'danger')

if __name__ == '__main__':
    # Print environment variables for debugging
    print(f"Environment variables:")
    print(f"MYSQL_HOST: {os.environ.get('MYSQL_HOST')}")
    print(f"MYSQL_USER: {os.environ.get('MYSQL_USER')}")
    print(f"MYSQL_DATABASE: {os.environ.get('MYSQL_DATABASE')}")
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)