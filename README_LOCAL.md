# 🚀 CRM Application - Local Setup Complete!

Your IT Platform CRM is ready to run on your local machine with Azure PostgreSQL.

---

## ✅ What's Ready

### Scripts & Configuration
- ✅ **migrate_db.py** - Creates all 8 tables with correct schema
- ✅ **seed_azure_db.py** - Populates database with sample data  
- ✅ **.env.template** - Configuration template with clear instructions
- ✅ **.gitignore** - Protects your .env file from being committed
- ✅ **requirements.txt** - All Python dependencies including python-dotenv

### Documentation
- 📖 **backend/QUICKSTART.md** - 5-minute setup guide (START HERE!)
- 📖 **backend/SETUP_LOCAL.md** - Comprehensive local setup guide
- 📖 **backend/README.md** - Database scripts reference
- 📖 **AZURE_DEV_SETUP.md** - Azure deployment guide

---

## 🎯 Get Started in 5 Minutes

### Step 1: Create Your .env File

```bash
cd backend
cp .env.template .env
```

Edit `.env` and replace with your Azure PostgreSQL credentials:
```bash
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASS@YOUR_SERVER.postgres.database.azure.com:5432/dev_psprawls?sslmode=require
```

### Step 2: Install & Setup

```bash
# Install Python dependencies
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup database (creates all tables with correct schema)
python migrate_db.py            # Drops and recreates all tables
python seed_azure_db.py         # Adds sample data
```

### Step 3: Run

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 7006 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Step 4: Access

- **Application:** http://localhost:5000
- **API Docs:** http://localhost:7006/docs

---

## 🔧 All Issues Fixed

### ✅ Database Schema
- All 8 tables created with correct columns
- `platforms` renamed to `platforms_crm` (avoids conflicts)
- `intake_requests` has all required columns: `dri_contact`, `submitted_for`, `help_types`

### ✅ Environment Configuration
- `.env.template` has clear instructions
- `migrate_db.py` loads `.env` file automatically
- `seed_azure_db.py` loads `.env` file automatically
- `.env` is protected by `.gitignore`

### ✅ Migration Scripts
- `migrate_db.py` - Safe mode (default) or `--drop` for fresh start
- `seed_azure_db.py` - Intelligent seeding, handles partial data
- Both scripts work on local machines with Azure PostgreSQL

---

## 📊 Sample Data Included

When you run `seed_azure_db.py`, you'll get:
- 3 Accounts (ACC001, ACC002, ACC003)
- 4 Use Cases across different platforms
- 4 Updates with timestamps
- 6 Platform onboarding records
- 3 Primary IT Partner assignments
- 7 Request States (New, In Review, Assigned, In Progress, Blocked, Completed, Rejected)
- 2 Sample Intake Requests with state assignments

---

## 🎓 Key Files for Your Reference

### Configuration
- `backend/.env` - Your database credentials (create from template)
- `backend/.env.template` - Template with examples

### Database Scripts  
- `backend/migrate_db.py` - Creates all tables
- `backend/seed_azure_db.py` - Adds sample data

### Documentation
- `backend/QUICKSTART.md` - **START HERE** for quick setup
- `backend/SETUP_LOCAL.md` - Detailed local setup guide
- `backend/README.md` - Database script documentation

### Application Code
- `backend/main.py` - FastAPI application & endpoints
- `backend/models.py` - Database models (SQLModel)
- `backend/database.py` - Database connection
- `frontend/src/` - React application

---

## 🐛 Troubleshooting

### Issue: "DATABASE_URL not set"
**Solution:** Make sure you created `.env` file and added your DATABASE_URL

### Issue: "column does not exist"  
**Solution:** Run `python migrate_db.py --drop` to recreate tables with correct schema

### Issue: "ModuleNotFoundError"
**Solution:** Activate virtual environment and run `pip install -r requirements.txt`

### Issue: Can't connect to database
**Solution:** Check your Azure PostgreSQL firewall rules allow your IP address

---

## 📝 Note About LSP Warnings

You may see 8 LSP diagnostics in `backend/models.py` about `__tablename__` attributes. These are harmless type-checking warnings from SQLModel's internal mechanics and **do not affect functionality**. The application works perfectly despite these warnings.

---

## 🚀 Next Steps

1. ✅ Set up your local environment
2. ✅ Create and test some accounts
3. ✅ Submit and manage intake requests  
4. 📖 See `AZURE_DEV_SETUP.md` when ready to deploy to Azure
5. 🎨 Customize the application for your team's needs!

---

**Need help?** Check the documentation files listed above or review the inline comments in the code.

**Ready to deploy?** See `AZURE_DEV_SETUP.md` for Azure App Service deployment.
