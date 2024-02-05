# Ecommerce-django

An E-commerce web application built with the Django framework. It allows users to browse, search, and purchase products from different categories. It uses Bootstrap for responsive and modern design, SQLite for database management, and Selenium for testing.

## Features

- User registration, login, logout, and profile management
- Product listing, filtering, and searching by category and name
- Product detail page with product variations and image gallery
- Shopping cart functionality with session and database storage
- Order history and status tracking
- User dashboard page with account information and order details

## Technologies

This project is built with [Django](https://www.djangoproject.com/) as the backend framework and uses the following technologies:

- Bootstrap to integrate Bootstrap.
- SQLite database engine.
- Selenium library for automated testing

## Installation and Usage

To run this project, you need to have Python 3.9 or higher and pip installed on your system.

Clone this repository and navigate to the project folder:

```sh
git clone https://github.com/itsmacr8/ecommerce-django.git
cd ecommerce-django
```

Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate
```

Apply the migrations:

```sh
python manage.py migrate
```

Create a superuser:

```sh
python manage.py createsuperuser
```

Run the development server and visit http://127.0.0.1:8000/ to see the application

```sh
python manage.py runserver
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
