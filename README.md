# Go Grocery

Go Grocery is a web-based grocery management system built with Flask. It provides functionalities for users to browse and order grocery products, and for administrators to manage categories, products, and view dashboard statistics.

## Features

- User registration, login, and logout
- Admin login and dashboard with statistics visualization
- CRUD operations for product categories and products
- Product browsing by category
- Shopping cart management with order placement and quantity updates
- Search functionality for categories and products
- Secure password hashing with Flask-Bcrypt
- User session management with Flask-Login
- Image upload support for product images

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd Go-Grocery-master
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Initialize the database and start the Flask development server:

   ```bash
   python run.py
   ```

2. Open your web browser and navigate to:

   ```
   http://127.0.0.1:5000/
   ```

## Usage

- **User Login:** Access the home page to log in as a user.
- **User Registration:** Register a new user account via the registration page.
- **Admin Login:** Access the admin login page at `/admin` to manage categories, products, and view dashboard stats.
- **Category and Product Management:** Admins can create, update, view, and delete categories and products.
- **Product Browsing:** Users can browse products by category and view product details.
- **Shopping Cart:** Users can add products to their cart, update quantities, and place orders.
- **Search:** Search for categories or products using the search functionality.

## Technologies Used

- Python 3
- Flask
- Flask-Bcrypt
- Flask-Login
- Flask-SQLAlchemy
- Flask-WTF
- SQLite (via SQLAlchemy)
- Matplotlib (for admin dashboard charts)
- Jinja2 templating

## License

This project is provided as-is without any explicit license.
