# Simple Banking App

A user-friendly and responsive Flask-based banking application designed for deployment on PythonAnywhere. This application allows users to create accounts, perform simulated money transfers between accounts, view transaction history, and securely manage their credentials.

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

## Getting Started

1. Clone the repository and install dependencies from `requirements.txt`.
2. Set up your `.env` file with MySQL and secret key settings.
3. Run `python app.py` to start the development server.
4. Access the app in your browser at `http://localhost:5000`.

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
