# Inventory Management

A Django inventory management application with a Bootstrap dashboard for managing products, categories, and stock levels. The dashboard supports product and category create, read, update, and delete operations. Django Admin is also available for administration.

## Requirements

- Python compatible with Django 6.1.2
- pip
- Internet access to load Bootstrap assets from the CDN

Python dependencies are listed in [`requirements.txt`](./requirements.txt).

## Setup

Run these commands from the project root (the directory containing `manage.py`).

### 1. Create and activate a virtual environment

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Create the database tables

```bash
python manage.py migrate
```

The project uses SQLite. Django creates the database file (`db.sqlite3`) in the project root when migrations are applied.

### 4. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email (if desired), and password. This account can sign in to Django Admin.

### 5. Collect static files and run with WhiteNoise and Gunicorn

```bash
python manage.py collectstatic --noinput
gunicorn inventory_management.wsgi:application --bind 127.0.0.1:8000 --workers 2 --threads 4
```

Open the dashboard at <http://127.0.0.1:8000/>. WhiteNoise serves the collected static files, and Gunicorn runs the Django WSGI application. The local default `DEBUG=True` keeps HTTPS redirects disabled. To manage users, visit <http://127.0.0.1:8000/admin/> and sign in with the superuser credentials.

On Windows, Gunicorn is not supported; use Django's development server instead:

```powershell
python manage.py runserver
```

## Using the dashboard

- Use **Add product** and **Add category** to create inventory records.
- Use the row action buttons to edit or delete products and categories.
- Search the products and categories using their respective search fields.
- Review the overview cards and low-stock section to monitor inventory.
- A category assigned to products cannot be deleted until those products are moved or deleted.

The dashboard uses Bootstrap assets from jsDelivr, so those styles and scripts require an internet connection.

## Deploying to Render

The included [`render.yaml`](./render.yaml) configures a Render web service and PostgreSQL database. In Render, create a new Blueprint from this repository and apply the generated configuration. The build command installs dependencies, collects static files for WhiteNoise, and applies database migrations; Gunicorn serves the application.

The Blueprint generates `SECRET_KEY` and configures PostgreSQL through `DATABASE_URL`. Render's filesystem is ephemeral, so the provisioned database keeps inventory data across deploys and restarts. The free PostgreSQL plan has a limited lifetime; choose a supported paid plan for ongoing production data.

For manual deployment, use these commands:

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --noinput
gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4
```

Set `SECRET_KEY`, `DATABASE_URL`, and `DEBUG=False` in the service environment. Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` only when overriding the Render defaults (comma-separated values).

## Project structure

```text
inventory_management/    Django project settings and root URL configuration
inventory/               Inventory app: models, forms, views, URLs, and migrations
inventory/templates/
  inventory/dashboard.html
manage.py                Django management command entry point
db.sqlite3               Local SQLite database, created after migration
```
