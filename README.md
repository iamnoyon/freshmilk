# FreshMilk

Milk delivery management system built with FastAPI.

## Prerequisites

- Python 3.12+
- PostgreSQL
- RabbitMQ

## Quick Start

```bash
# Clone
git clone https://github.com/iamnoyon/freshmilk.git
cd freshmilk

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template
copy .env.example .env
# Edit .env with your actual credentials

# Run database migrations (manual)
# 1. Create PostgreSQL database: freshmilk
# 2. Apply enum types and column migrations

# Start
uvicorn app.main:app --reload
```

## Environment Variables

| Variable | Description |
|---|---|
| `JWT_SECRET` | Secret key for JWT signing |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes |
| `SMS_API_KEY` | SMS provider API key |
| `SMS_API_URL` | SMS provider API URL |
| `RABBITMQ_HOST` | RabbitMQ host |
| `RABBITMQ_PORT` | RabbitMQ port |
| `RABBITMQ_USER` | RabbitMQ username |
| `RABBITMQ_PASS` | RabbitMQ password |

## Database

The project uses PostgreSQL. You need to manually create the database and apply migrations:

```sql
CREATE DATABASE freshmilk;

-- Enum types
CREATE TYPE roleenum AS ENUM ('customer', 'deliveryman', 'admin', 'superadmin');
CREATE TYPE areaenum AS ENUM ('mirpurdosh');

-- Tables are auto-created on first run via SQLAlchemy
```

On first startup, a superadmin is seeded:
- Phone: `0000000000`
- Password: `admin123`
