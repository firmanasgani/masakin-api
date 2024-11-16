# Masakin API

## Overview

Masakin is a RESTful API built with Flask, providing endpoints for managing recipes. This project leverages modern technologies such as Flask-Smorest, Flask-Migrate, Flask-JWT-Extended, and Flask-CORS.

## Features

- **JWT Authentication**: Secure endpoints with access and refresh tokens.
- **Database Migrations**: Powered by Flask-Migrate.
- **Cross-Origin Resource Sharing (CORS)**: Enabled for cross-domain requests.

## Installation

### Prerequisites

- Python 3.8 or higher
- `pipenv` (Python environment and dependency manager)
- A MySQL database 

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Step 2: Install Dependencies
```bash
pipenv install
```

### Step 3: Activate the Virtual Environment
```bash
pipenv shell
```

### Step 4: Configure Environment Variables
Create a .env file in the root directory based on .env.example:

```bash
cp .env.example .env
```

Edit the .env file to include your configuration:

```bash
DATABASE_URI=mysql+mysqlconnector://<user>:<password>@<host>/<database>
JWT_SECRET_KEY=<your-secret-key>
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

### Step 5: Run Database Migrations
```bash
flask db upgrade
```

### Step 6: Seed the Database
```bash
pipenv run python -m seeders.seed
```

### Step 7: Start the Server
```bash
flask run
```

## Project Structure
```bash
├── connectors/                    # Custom database or service connectors
│   └── __init__.py
├── controllers/                   # API controllers for handling requests
│   ├── __init__.py
│   └── recipes_controller.py
├── migrations/                    # Alembic database migration files
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 78be99a45234_add_updated_at_and_set_timestamp_.py
│       └── 87b22d769247_recipes_migration.py
├── models/                        # Database models
│   ├── __init__.py
│   └── recipe.py
├── response/                      # Custom response utilities
│   └── response_builder.py
├── schemas/                       # Schema definitions for request/response validation
│   ├── __init__.py
│   └── recipe.py
├── seeders/                       # Seed scripts for populating the database
│   ├── __init__.py
│   └── seed_recipes.py
├── utils/                         # Utility functions
│    └── __init__.py
├── db.py                          # Database initialization
├── Pipfile
├── Pipfile.lock
├── README.md
├── app.py                         # Main application entry point
```