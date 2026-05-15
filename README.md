# Restaurant Reservation System

A modern web application for restaurant table reservations built with Flask and PostgreSQL.

## Features

- User authentication (registration and login)
- Browse restaurant menu
- Make and manage reservations
- Admin panel for managing reservations and menu
- Responsive design for all devices

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render.com

## Project Structure

```
restaurant-reservation-app/
├── app/
│   ├── routes/           # Flask blueprints for routes
│   ├── templates/        # HTML templates
│   ├── static/
│   │   ├── css/         # CSS stylesheets
│   │   └── js/          # JavaScript files
│   ├── models.py        # Database models
│   └── __init__.py      # App factory
├── config.py            # Configuration settings
├── run.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env               # Environment variables (local development)
└── README.md          # This file
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
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**
   - Create a new PostgreSQL database: `restaurant_db`
   - Update `.env` with your database credentials

5. **Run the application**
   ```bash
   python run.py
   ```
   
   The app will be available at `http://localhost:5000`

## Deployment on Render.com

### Prerequisites
- GitHub account with the project repository
- Render.com account

### Deployment Steps

1. Connect your GitHub repository to Render.com
2. Create a new Web Service
3. Configure the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
4. Add environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
   - Database credentials from Render PostgreSQL
5. Deploy and wait for build completion

## Database Models

### User
- id (Primary Key)
- username
- email
- password_hash
- created_at

### Restaurant
- id (Primary Key)
- name
- description
- address
- phone
- opening_hours

### MenuItem
- id (Primary Key)
- restaurant_id (Foreign Key)
- name
- description
- price
- category

### Reservation
- id (Primary Key)
- user_id (Foreign Key)
- restaurant_id (Foreign Key)
- reservation_date
- reservation_time
- party_size
- special_requests
- created_at

## API Routes

### Public Routes
- `GET /` - Home page
- `GET /menu` - Menu display
- `GET /reserve` - Reservation page
- `GET /about` - About page
- `GET /contact` - Contact page

### Authentication Routes
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Protected Routes (Coming Soon)
- `GET /dashboard` - User dashboard
- `GET/POST /reservations` - Manage reservations
- `GET /admin` - Admin panel

## Contributing

This is an educational project. Feel free to extend and modify as needed.

## License

MIT License - Feel free to use this project for learning purposes.

## Author

Created as an academy assignment - Restaurant Reservation System
