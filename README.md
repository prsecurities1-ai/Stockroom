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

### 5. Start the development server

```bash
python manage.py runserver
```

Open the dashboard at <http://127.0.0.1:8000/>. To manage users and access the Django administration site, visit <http://127.0.0.1:8000/admin/> and sign in with the superuser credentials.

## Using the dashboard

- Use **Add product** and **Add category** to create inventory records.
- Use the row action buttons to edit or delete products and categories.
- Search the products and categories using their respective search fields.
- Review the overview cards and low-stock section to monitor inventory.
- A category assigned to products cannot be deleted until those products are moved or deleted.

The dashboard uses Bootstrap assets from jsDelivr, so those styles and scripts require an internet connection.

## Project structure

```text
inventory_management/    Django project settings and root URL configuration
inventory/               Inventory app: models, forms, views, URLs, and migrations
inventory/templates/
  inventory/dashboard.html
manage.py                Django management command entry point
db.sqlite3               Local SQLite database, created after migration
```
