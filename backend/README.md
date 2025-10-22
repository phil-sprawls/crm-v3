# Backend Directory

FastAPI backend for IT Platform CRM application.

## 🚀 Quick Start (Local Machine)

See **`QUICKSTART.md`** for step-by-step setup guide!

**TL;DR:**
```bash
# 1. Setup
cd backend
cp .env.template .env          # Edit .env with your database credentials
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Database
python migrate_db.py           # Create all tables (drops existing!)
python seed_azure_db.py        # Add sample data

# 3. Run
uvicorn main:app --host 0.0.0.0 --port 7006 --reload
```

**Access API docs:** http://localhost:7006/docs

## Database Scripts

### migrate_db.py
Creates all database tables for the CRM application.

**Usage:**
```bash
python migrate_db.py
```

**What it does:**
- **ALWAYS drops and recreates all tables from scratch**
- Creates all 8 database tables with exact schema from models.py:
  - `accounts` - Main account/team information (24 columns)
  - `use_cases` - Use cases for each account (9 columns)
  - `updates` - Activity updates (6 columns)
  - `platforms_crm` - Platform onboarding status (4 columns)
  - `primary_it_partners` - IT partner assignments (3 columns)
  - `request_states` - Workflow states for intake requests (5 columns)
  - `intake_requests` - User-submitted assistance requests (11 columns)
  - `request_state_assignments` - Request-to-state relationships (4 columns)
- Inserts 7 default request states
- Ensures all columns match models.py exactly
- Prevents column mismatch errors

**When to use:**
- Setting up new database
- Fixing column mismatches
- After updating models.py
- Any time you need a fresh database schema

**⚠️ Warning:** This script DELETES ALL DATA every time it runs!

### seed_azure_db.py
Seeds Azure PostgreSQL database with sample data.

**Usage:**
```bash
python seed_azure_db.py
```

**What it does:**
- Creates 3 sample accounts
- Creates 3 use cases
- Creates 3 updates
- Creates 6 platform records
- Creates 3 IT partner records
- Creates 7 request states (if not present)
- Creates 2 sample intake requests
- Assigns states to requests

**When to use:**
- Initial Azure database setup
- Testing/demo environment
- Development environment with Azure PostgreSQL

---

## Environment Variables

Copy the template and fill in your values:

```bash
cp .env.template .env
```

Then edit `.env` with the following variables:

### Required
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dev_psprawls
USE_SAMPLE_DATA=false
```

### Optional - JWT Authentication
```bash
APP_CLIENT_ID=your-azure-ad-app-client-id
TENANT_ID=your-azure-tenant-id
OPENAPI_CLIENT_ID=your-openapi-client-id
```

### Optional - Email Notifications
```bash
ADMIN_EMAIL=admin@yourcompany.com
AZURE_COMMUNICATION_CONNECTION_STRING=your-connection-string
```

## API Documentation

When the server is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI application and endpoints
├── models.py            # SQLModel database models
├── database.py          # Database connection
├── sample_data.py       # In-memory sample data
├── migrate_db.py        # Database migration script
├── seed_azure_db.py     # Azure database seeding script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── test_main.py         # Test suite
```

## Testing

```bash
pytest
```

## Deployment

See **AZURE_DEV_SETUP.md** in the project root for complete Azure deployment instructions.
