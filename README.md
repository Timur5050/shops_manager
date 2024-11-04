## Project Description

This RESTful API application enables users to manage web shops and their products. It provides secure user authentication through JWT-based token access, and it’s designed for easy scalability with Docker and Docker Compose. Users can create, view, and manage shops and products, all stored in a PostgreSQL database with caching and asynchronous capabilities.

## Key Features
- JWT Authentication: Secure login with token-based access control
- User Registration and Login: Easy account management with token refreshing
- Database Caching: Redis for efficient data caching
- Asynchronous Tasks: Background task processing
- SQLAlchemy & Pydantic: Database ORM and data validation
- Alembic Migrations: Manage database schema changes
- Middleware Support: Customizable middleware for request handling
- Comprehensive Documentation
- Dockerized Deployment: Docker and Docker Compose for containerization
- Permissions: Access control for users


## Main functionality
1. Shop Management
    - Create a new shop
    - View all shops
    - Access only the shops related to the current user
    - View shop details, including a list of products within it
      
2. Product Management
    - Add products to specific shops
    - Delete products from your shops
    - Bulk upload products (e.g., from an Excel file) with asynchronous processing
    - Filter products by availability
    - Retrieve product details by ID

3. User Authentication and Authorization
    - Registration: New users can register with a username and password
    - Login: Users receive access and refresh tokens upon logging in
    - Token Refresh: Renew access tokens with a valid refresh token

## how to run 
```sh
# Clone the repository
git clone https://github.com/Timur5050/shops_manager.git
# Change to the project directory
cd shops_manager
# Set up a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# Install required packages
pip install -r requirements.txt
# create directory in project with files encoders(private and public keys): private.pem and public.pem
# Add an .env file, following the structure provided in sample.env
# Set Up Alembic for Database Migrations
# alembic init alembic
# Add your database URL to alembic.ini under sqlalchemy.url.
# Import all models into alembic/env.py and set target_metadata = Base.metadata.
# build and start docker compose
docker-compose build
# then start containers
docker-compose up
# Go to http://127.0.0.1:8001/doc - swagger documentation
#  http://127.0.0.1:8001/ - API endpoint
```

