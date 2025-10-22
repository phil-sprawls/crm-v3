# Local Machine Setup Guide

Complete step-by-step guide for running this CRM application on your local machine with Azure PostgreSQL.

## Prerequisites

- Python 3.11+ installed
- Node.js 20+ installed
- Git (to clone the repository)
- Azure PostgreSQL database (or connection string)

---

## Step 1: Clone and Navigate

```bash
# If cloning from GitHub
git clone <your-repo-url>
cd <your-repo-name>

# Or if already have the files
cd /path/to/your/crm-app
```

---

## Step 2: Backend Setup

### 2a. Install Python Dependencies

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2b. Configure Environment Variables

```bash
# Copy the template
cp .env.template .env

# Open .env in your editor
# On Mac/Linux:
nano .env
# or
code .env  # if using VS Code

# On Windows:
notepad .env
```

**Edit `.env` file and add your Azure PostgreSQL connection string:**

```bash
# Required - Your Azure PostgreSQL connection string
DATABASE_URL=postgresql://username:password@your-server.postgres.database.azure.com:5432/dev_psprawls?sslmode=require

# Optional - For sample data mode (not needed for Azure)
USE_SAMPLE_DATA=false

# Optional - For email notifications
ADMIN_EMAIL=your-email@company.com
AZURE_COMMUNICATION_CONNECTION_STRING=your-azure-comm-string
```

**Example with real values:**
```bash
DATABASE_URL=postgresql://dbadmin:MyP@ssw0rd@myserver.postgres.database.azure.com:5432/dev_psprawls?sslmode=require
USE_SAMPLE_DATA=false
```

### 2c. Run Database Migration

```bash
# Create all tables with correct schema
python migrate_db.py

# If you get column errors or need fresh start:
python migrate_db.py --drop
```

**Expected output:**
```
============================================================
Database Migration - IT Platform CRM
============================================================
🚀 Starting database migration...
📍 Connecting to: your-server.postgres.database.azure.com:5432/dev_psprawls
📋 Creating accounts table...
✅ accounts table created
...
🎉 Migration completed successfully!
```

### 2d. Seed Sample Data (Optional)

```bash
# Add sample data for testing
python seed_azure_db.py
```

**Expected output:**
```
============================================================
Azure Database Seeding Script
============================================================
🔌 Connecting to Azure PostgreSQL database...
✅ Connected successfully
...
🎉 Database seeding completed successfully!
```

---

## Step 3: Frontend Setup

### 3a. Install Node Dependencies

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

### 3b. Configure API URL (Optional)

The frontend automatically detects the correct API URL. For local development:
- Frontend runs on: http://localhost:5000
- Backend API runs on: http://localhost:8000

No additional configuration needed!

---

## Step 4: Run the Application

You have two options:

### Option A: Run Both (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Mac/Linux
# or venv\Scripts\activate on Windows

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option B: Run Backend Only (API Testing)

```bash
cd backend
source venv/bin/activate  # Mac/Linux
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Access API docs at: http://localhost:8000/docs

---

## Step 5: Access the Application

Open your browser and navigate to:
- **Frontend Application**: http://localhost:5000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## Common Issues and Solutions

### Issue: "DATABASE_URL environment variable not set"

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Verify .env file exists
ls -la .env

# Check .env file has DATABASE_URL
cat .env | grep DATABASE_URL

# Make sure you activated virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Issue: "column dri_contact does not exist"

**Solution:**
```bash
# Drop and recreate tables with correct schema
cd backend
python migrate_db.py --drop
python seed_azure_db.py
```

### Issue: Frontend can't connect to backend

**Solution:**
1. Make sure backend is running on port 8000
2. Check backend logs for errors
3. Verify no firewall is blocking port 8000

### Issue: "ModuleNotFoundError: No module named 'dotenv'"

**Solution:**
```bash
cd backend
pip install python-dotenv
# or
pip install -r requirements.txt
```

---

## Verifying Everything Works

### 1. Test Database Connection
```bash
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('DATABASE_URL:', os.getenv('DATABASE_URL')[:50] + '...')"
```

### 2. Test Backend API
```bash
# In browser, visit:
http://localhost:8000/docs

# Or use curl:
curl http://localhost:8000/api/accounts
```

### 3. Test Frontend
```bash
# In browser, visit:
http://localhost:5000
```

---

## Quick Reference Commands

```bash
# Start backend (from project root)
cd backend && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend (from project root)
cd frontend && npm run dev

# Recreate database
cd backend && python migrate_db.py --drop && python seed_azure_db.py

# Check database
cd backend && python -c "from sqlalchemy import create_engine, text; from dotenv import load_dotenv; import os; load_dotenv(); engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); result = conn.execute(text('SELECT COUNT(*) FROM accounts')); print('Accounts:', result.scalar())"
```

---

## File Structure Reference

```
your-project/
├── backend/
│   ├── .env                # Your local config (DO NOT COMMIT)
│   ├── .env.template       # Template for .env
│   ├── requirements.txt    # Python dependencies
│   ├── main.py            # FastAPI application
│   ├── models.py          # Database models
│   ├── database.py        # Database connection
│   ├── migrate_db.py      # Migration script
│   ├── seed_azure_db.py   # Seeding script
│   └── venv/              # Virtual environment (DO NOT COMMIT)
├── frontend/
│   ├── src/               # React source code
│   ├── package.json       # Node dependencies
│   └── node_modules/      # Node packages (DO NOT COMMIT)
└── README.md
```

---

## Next Steps

1. ✅ Database is set up with sample data
2. ✅ Backend API is running
3. ✅ Frontend is running
4. 🚀 Start building your custom features!
5. 📖 See AZURE_DEV_SETUP.md for Azure deployment guide

---

## Need Help?

- Check `backend/README.md` for database script details
- Check `AZURE_DEV_SETUP.md` for Azure-specific setup
- Check `LOCAL_SETUP.md` for additional local setup info
