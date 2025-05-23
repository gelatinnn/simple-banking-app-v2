import os
import logging
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer
from flask_wtf.csrf import CSRFProtect
from flask_limiter.errors import RateLimitExceeded
import pymysql
import secrets
from datetime import timedelta

# Import extensions
from extensions import db, login_manager, bcrypt, limiter

# Load environment variables
load_dotenv()

# Initialize CSRF protection
csrf = CSRFProtect()

# MySQL connection
pymysql.install_as_MySQLdb()

# Set up audit logging
logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Helper function for audit logging

def audit_log(message):
    logging.info(message)

# Step 1: Create Flask application with secure session management
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

    # --- Secure Session Settings ---
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if using HTTPS in production!
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Auto-logout after 30 min inactivity
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

    # CSRF Protection
    csrf.init_app(app)

    # Database configuration
    mysql_user = os.environ.get('MYSQL_USER', '')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_host = os.environ.get('MYSQL_HOST', '')
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_database = os.environ.get('MYSQL_DATABASE', '')

    mysql_port = str(mysql_port)
    if not mysql_host or not mysql_user or not mysql_database:
        print(f"WARNING: Missing database configuration. Host: {mysql_host}, User: {mysql_user}, Database: {mysql_database}")

    db_uri = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
 
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set secure cookie flags for session cookies
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Prevent CSRF via cross-site requests

    # Set session timeout (30 minutes of inactivity)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)

    # Register custom error handler for rate limiting
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        if request.path.startswith('/api/') or request.headers.get('Accept') == 'application/json':
            return jsonify({"error": "Rate limit exceeded", "message": str(e)}), 429
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

    # Set security headers for all responses
    @app.after_request
    def set_security_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' https://cdn.jsdelivr.net; font-src 'self' https://cdn.jsdelivr.net; script-src 'self' https://cdn.jsdelivr.net;"
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return response

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # --- Privacy Policy and Terms of Service routes ---
    @app.route('/privacy-policy')
    def privacy_policy():
        return render_template('privacy_policy.html', title='Privacy Policy')

    @app.route('/terms-of-service')
    def terms_of_service():
        return render_template('terms_of_service.html', title='Terms of Service')

    return app

# Step 2: Create Flask app
app = create_app()

# Step 3: Enforce session timeout and refresh on every request
@app.before_request
def make_session_permanent():
    session.permanent = True

# Step 4: Import models after db initialization
from models import User, Transaction

# Step 5: User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Step 6: Import routes after app creation
from routes import *

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

if __name__ == '__main__':
    print("\nApp running at: http://localhost:5000\n")

    print(f"MYSQL_HOST: {os.environ.get('MYSQL_HOST')}")
    print(f"MYSQL_USER: {os.environ.get('MYSQL_USER')}")
    print(f"MYSQL_DATABASE: {os.environ.get('MYSQL_DATABASE')}")
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    