# IMT Bank

[Live Demo on PythonAnywhere](https://wejasa1637.pythonanywhere.com/login?next=%2F )

A user-friendly and responsive Flask-based banking application designed for deployment on PythonAnywhere. This application allows users to create accounts, perform simulated money transfers between accounts, view transaction history, and securely manage their credentials.

---

## Table of Contents
- [New Security Features & Enhancements (2025)](#new-security-features--enhancements-2025)
- [Group Members](#group-members)
- [Features](#features)
- [Security Overview](#security-overview)
- [Automated Security Assessment Scripts](#automated-security-assessment-scripts)
- [Getting Started](#getting-started)
- [Database Setup](#database-setup)
- [How to Use Security Scripts](#how-to-use-security-scripts)
- [Deploying to PythonAnywhere](#deploying-to-pythonanywhere)
- [Usage](#usage)
- [User Roles](#user-roles)
- [Address Management](#address-management)
- [Technologies Used](#technologies-used)
- [Rate Limiting](#rate-limiting)
- [License](#license)

---


## New Security Features & Enhancements (2025)
- Strong password policy (min 8 chars, upper/lowercase, number, special char)
- CSRF protection for all forms (Flask-WTF)
- Session security: Secure, HttpOnly, SameSite cookies; 30-min inactivity logout
- Rate limiting on login, registration, and sensitive endpoints (Flask-Limiter)
- Account lockout after multiple failed logins
- Audit logging for critical actions
- Custom error pages (400, 403, 404, 500)
- Input validation and XSS protection (Jinja2 auto-escaping)
- Admin/Manager dashboards for user and transaction management
- Legal pages: Privacy Policy, Terms of Service
- Accessibility improvements (ARIA roles, keyboard navigation)

---

## Group Members
- Aron Ibias [AronIbias21]
- Jester Tapit [TAPIT08]
- Maria Angela Matubis[gelatinnn]

---

## Features

- **User Authentication**
  - Secure login with username/password
  - Registration of new users
  - Password recovery mechanism (email-based)
- **Account Management**
  - Display of account balance
  - View recent transaction history (last 10 transactions)
- **Fund Transfer**
  - Transfer money to other registered users
  - Confirmation screen before completing transfers
  - Transaction history updated after transfers
- **User Role Management**
  - Regular user accounts
  - Admin users with account approval capabilities
  - Manager users who can manage admin accounts
- **Location Data Integration**
  - Philippine Standard Geographic Code (PSGC) API integration
  - Hierarchical location data selection (Region, Province, City, Barangay)
  - Form fields pre-populated with location data
- **Admin Features**
  - User account approval workflow
  - Account activation/deactivation
  - Deposit funds to user accounts
  - Create new accounts
  - Edit user information
- **Manager Features**
  - Create and manage admin accounts
  - View admin transaction logs
  - Monitor all system transfers
- **Security**
  - Password hashing with bcrypt for secure storage
  - Secure session management (secure cookies, session timeout, HttpOnly, SameSite, 30 min inactivity logout)
  - Token-based password reset
  - API rate limiting to prevent abuse (Flask-Limiter, with Redis support)
  - CSRF protection for all forms
  - Input validation and strong password policy (min 8 chars, upper/lowercase, digit, special char)
  - Output encoding and XSS protection (Jinja2 auto-escaping)
  - Graceful error handling with user-friendly error pages (400, 403, 404, 500)
  - Accessibility improvements (ARIA roles, labels, keyboard navigation)
  - User notifications for all critical actions (login, logout, transfer, registration, errors)

---

## Security Overview

- Strong password policy and validation
- Passwords hashed with bcrypt
- Secure session management (cookie flags, timeout)
- CSRF protection for all forms
- Rate limiting on sensitive endpoints
- Generic error handlers and user-friendly error pages
- Jinja2 auto-escaping enforced
- Secrets/credentials loaded from environment variables
- Audit logging for sensitive actions
- Clickjacking protection via headers

---


## Getting Started

### Prerequisites
- Python 3.7+
- pip
- MySQL Server 5.7+ or MariaDB 10.2+

### Installation
1. **Clone the repository:**
   ```
   git clone https://github.com/gelatinnn/simple-banking-app-v2.git
   cd simple-banking-app-v2
   ```
2. **Install required packages:**
   ```
   pip install -r requirements.txt
   ```
3. **Set up your `.env` file:**
   ```
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_DATABASE=simple_banking
   SECRET_KEY=your_secret_key
   ```
4. **Initialize the database:**
   ```
   python init_db.py
   ```
5. **Run the application:**
   ```
   python app.py
   ```
6. **Access at:** `http://localhost:5000`

---
## Database Setup

1. **Install MySQL Server or XAMPP (with MariaDB)**
2. **Create a database user and set privileges:**
   ```
   mysql -u root -p
   CREATE DATABASE simple_banking;
   CREATE USER 'bankapp'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON simple_banking.* TO 'bankapp'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```
3. **Update the `.env` file** as shown above.
4. **Initialize the database:**
   ```
   python init_db.py
   ```
---

## Usage

### Registration
- Navigate to the registration page
- Enter username, email, and password (see password policy below)
- Confirm your password
- Submit the form to create your account (pending admin approval)

### Login
- Enter your username and password
- Click "Sign In"

### Account Overview
- View your current balance
- See your recent transaction history

### Transfer Funds
- Navigate to the Transfer page
- Enter recipient's username or account number
- Enter the amount to transfer
- Confirm the transfer details on the confirmation screen
- Complete the transfer

### Password Reset
- Click "Forgot your password?" on the login page
- Enter your registered email address
- Follow the link in the email (simulated in this demo)
- Create a new password (must meet password policy)

### Admin Features
- Approve new user registrations
- Activate/deactivate user accounts
- Create new user accounts
- Make over-the-counter deposits to user accounts
- Edit user details including location information

### Manager Features
- Create new admin accounts
- Toggle admin status for users
- View all user transactions
- Monitor and audit admin activities

## User Roles

The system supports three types of user roles:

1. **Regular Users** - Can manage their own account, make transfers, and view their transaction history.
2. **Admin Users** - Have all regular user privileges plus:
   - Approve/reject new user registrations
   - Activate/deactivate user accounts
   - Create new user accounts
   - Make deposits to user accounts
   - Edit user information
3. **Manager Users** - Have all admin privileges plus:
   - Create and manage admin accounts
   - View admin transaction logs
   - Monitor all system transfers
   - System-wide oversight capabilities

## Address Management with PSGC API

The application integrates with the Philippine Standard Geographic Code (PSGC) API to provide standardized address selection for user profiles. The address system follows the Philippine geographical hierarchy:
- Region
- Province
- City/Municipality
- Barangay

This integration ensures addresses are standardized and validates location data according to the Philippine geographical structure.

## Security and Best Practices

- All sensitive data (passwords, session cookies) are securely stored and transmitted.
- Session cookies use `Secure`, `HttpOnly`, and `SameSite=Strict` flags.
- Sessions expire after 30 minutes of inactivity.
- All forms are protected with CSRF tokens.
- Passwords must be at least 8 characters, include uppercase, lowercase, a digit, and a special character.
- All user input is validated on both client and server side.
- All user actions provide clear feedback via notifications.
- Error pages (400, 403, 404, 500) are user-friendly and do not leak sensitive information.
- Accessibility is considered throughout the UI (ARIA roles, keyboard navigation, labels).

## Technologies Used

- **Backend**: Python, Flask
- **Database**: MySQL (with SQLAlchemy ORM)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Authentication**: Flask-Login, Werkzeug, Flask-Bcrypt
- **Forms**: Flask-WTF, WTForms
- **Security**: Flask-Limiter for API rate limiting, CSRF protection
- **External API**: PSGC API for Philippine geographic data

## Rate Limiting

The application uses Flask-Limiter to implement API rate limiting, which protects against potential DoS attacks and abusive bot activity. The rate limits are configured as follows:

- **Login**: 10 attempts per minute
- **Registration**: 5 attempts per minute
- **Password Reset**: 5 attempts per hour
- **Money Transfer**: 20 attempts per hour
- **API Endpoints**: 30 requests per minute
- **Admin Dashboard**: 60 requests per hour
- **Admin Account Creation**: 20 accounts per hour
- **Admin Deposits**: 30 deposits per hour
- **Manager Dashboard**: 60 requests per hour
- **Admin Creation**: 10 admin accounts per hour

By default, the rate limiting data is stored in memory. For production use, it's recommended to use Redis as a storage backend for persistence across application restarts. To enable Redis storage:

1. Install Redis server on your system
2. Update the `.env` file with your Redis URL:
   ```
   REDIS_URL=redis://localhost:6379/0
   ```
If Redis is not available, the application will automatically fall back to in-memory storage.

## License

MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
