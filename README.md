# Restaurant Reservation System

A modern web application for restaurant table reservations built with Flask and PostgreSQL.

## Features

- User authentication (registration and login)
- Browse and filter restaurant menu by category
- Make and manage reservations
- Cancel reservations
- Leave and view reviews
- View special offers and promotions
- Contact form
- Admin panel for managing reservations, menu, users and specials
- Responsive design for all devices

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: PostgreSQL (production), SQLite (local development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render.com

## Project Structure

```
restaurant-reservation-app/
├── app/
│   ├── routes/
│   │   ├── main.py       # Public routes
│   │   ├── auth.py       # Authentication routes
│   │   ├── dashboard.py  # User dashboard routes
│   │   └── admin.py      # Admin panel routes
│   ├── templates/        # HTML templates
│   ├── static/
│   │   ├── css/          # CSS stylesheets
│   │   └── js/           # JavaScript files
│   ├── models.py         # Database models
│   └── __init__.py       # App factory
├── config.py             # Configuration settings
├── wsgi.py               # WSGI entry point for production
├── run.py                # Entry point for local development
├── seed_data.py          # Script to seed the database
├── render.yaml           # Render.com deployment config
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd restaurant-reservation-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Mac/Linux: source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

   The app will be available at `http://localhost:5000`

   > Local development uses SQLite — no database setup required.

## Deployment on Render.com

### Prerequisites
- GitHub account with the project repository
- Render.com account

### Deployment Steps

1. Connect your GitHub repository to Render.com
2. Render will detect `render.yaml` at the project root and configure the service automatically
3. Go to your web service → **Environment** tab and add the following from your Render PostgreSQL database:
   - `DB_HOST`
   - `DB_PORT`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
4. Deploy and wait for build completion

> **Note**: Never hardcode database credentials in your code. Always use environment variables.

## Database Models

### User
- id, username, email, password_hash, created_at

### Restaurant
- id, name, description, address, phone, opening_hours

### MenuItem
- id, restaurant_id, name, description, price, category, available

### Reservation
- id, user_id, restaurant_id, reservation_date, reservation_time, party_size, special_requests, status, created_at

### Review
- id, user_id, restaurant_id, rating, title, comment, created_at

### Special
- id, restaurant_id, title, description, discount, valid_until, created_at

### ContactMessage
- id, name, email, phone, subject, message, created_at

## Routes

### Public
- `GET /` - Home page
- `GET /menu` - Menu display
- `GET /menu/filter` - Filter menu by category
- `GET /search` - Search menu items
- `GET /reserve` - Reservation page
- `GET /about` - About page
- `GET /contact` - Contact form
- `GET /reviews` - Reviews page
- `GET /specials` - Special offers page

### Authentication
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Dashboard (login required)
- `GET /dashboard` - User dashboard
- `GET /dashboard/reservations` - Manage reservations
- `GET /dashboard/profile` - User profile

### Admin (login required)
- `GET /admin` - Admin dashboard
- `GET /admin/reservations` - Manage reservations
- `GET /admin/menu` - Manage menu items
- `GET /admin/users` - Manage users
- `GET /admin/specials` - Manage special offers

## Author

Created as an academy assignment - Restaurant Reservation System
