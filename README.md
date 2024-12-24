# Budget App

A zero-based budgeting application with bank integration built with Django, HTMX, and TailwindCSS.

## Features

- Email-based authentication with social login options (Google, LinkedIn, Microsoft)
- Two-factor authentication (2FA) required for all users
- Bank account integration via Plaid API
- Zero-based budgeting system
- Custom pay period support
- Automatic transaction imports
- Recurring transaction management

## Tech Stack

- **Backend**: Django 5.1
- **Frontend**: 
  - TailwindCSS for styling
  - HTMX for dynamic interactions
  - Custom theme app for component organization
- **Authentication**: django-allauth with custom user model
- **API Integration**: Plaid API for bank connections
- **Security**: 2FA, HTTPS enforced in production

## Prerequisites

- Python 3.12+
- Node.js 18+ and npm (for TailwindCSS)
- Virtual environment tool (venv recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd budget_app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Install frontend dependencies and build CSS:
   ```bash
   cd theme/static_src
   npm install
   npm run build
   ```

6. Run database migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Development

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Watch for CSS changes:
   ```bash
   cd theme/static_src
   npm run dev
   ```

## Testing

Run the test suite:
```bash
pytest
```

## Environment Variables

Required environment variables:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to True for development
- `DATABASE_URL`: Database connection string
- `PLAID_CLIENT_ID`: Plaid API client ID
- `PLAID_SECRET`: Plaid API secret key
- `PLAID_ENVIRONMENT`: Plaid environment (sandbox/development/production)

Social authentication credentials:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `LINKEDIN_CLIENT_ID`
- `LINKEDIN_CLIENT_SECRET`
- `MICROSOFT_CLIENT_ID`
- `MICROSOFT_CLIENT_SECRET`

## Project Structure

- `accounts/`: Custom user model and authentication
- `banking/`: Bank account integration and Plaid API
- `budgets/`: Budget management and calculations
- `transactions/`: Transaction handling and categorization
- `theme/`: TailwindCSS and templates
- `core/`: Project settings and configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
