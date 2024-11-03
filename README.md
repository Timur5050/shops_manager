## Project Description

This application allows users to manage their web-shops and manage products in them through a REST API. The application includes user authentication and token-based access control (JWT). Users can register, log in, manage shops, products, which are stored in a database. 

## Main features
1. Shops management
   - create shop
   - get all shops 
   - get shop than relate to current user
   - get details of some shop with the list of products in it

2. Products management
   - create product to one of your shops
   - delete product from one of your shops
   - load many products, for instanse, load many products from xls. async function, so tou do not need to wait the end of fetching all products
   - get products from some shop, also with filtering, whether the product is available or not
   - retrieve product by its id

3. User Authentication and JWT
   -  User Registration: New users can register by providing a username and password.
   -  User Login: Users can log in with their credentials, receiving access and refresh tokens.
   -  Token Refresh: Users can refresh their access tokens using a valid refresh token.

## how to run 
```sh
# Clone the repository
git clone https://github.com/Timur5050/shops_manager.git
# Change to the project directory
cd shops_manager
# Create a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# Install required packages
pip install -r requirements.txt
# create directory in project with files encoders(private and public keys): private.pem and public.pem
# create .env file and fill it with data as in sample.env
# alembic init alembic
# enter database url into alembic.ini to the varialbe -> sqlalchemy.url and import there all 
```

