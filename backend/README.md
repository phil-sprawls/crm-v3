# Backend Directory

FastAPI backend for IT Platform CRM application.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Database Scripts

### migrate_db.py
Creates all database tables for the CRM application.

**Usage:**
```bash
# Safe mode - preserves existing data
python migrate_db.py

# Drop and recreate all tables (DESTRUCTIVE - deletes all data)
python migrate_db.py --drop
```

**What it does:**
- Creates all 8 database tables with exact schema from models.py:
  - `accounts` - Main account/team information
  - `use_cases` - Use cases for each account
  - `updates` - Activity updates
  - `platforms_crm` - Platform onboarding status
  - `primary_it_partners` - IT partner assignments
  - `request_states` - Workflow states for intake requests
  - `intake_requests` - User-submitted assistance requests
  - `request_state_assignments` - Request-to-state relationships
- Inserts 7 default request states
- Safe mode: uses CREATE TABLE IF NOT EXISTS (preserves data)
- Drop mode: drops all tables and recreates from scratch

**When to use:**
- **Safe mode**: Setting up new database, adding missing tables
- **Drop mode**: Fixing column mismatches, starting fresh, recovering from corruption

**⚠️ Warning:** `--drop` flag will delete ALL data! Use with caution.

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
