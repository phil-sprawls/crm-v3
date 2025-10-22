# Quick Start - Local Machine Setup

**Get your CRM running on your local machine in 5 minutes!**

## Step 1: Create .env File (1 minute)

```bash
cd backend

# Copy the template
cp .env.template .env

# Edit with your Azure database credentials
# Use your favorite editor (nano, vim, VS Code, notepad, etc.)
nano .env
```

**Replace these placeholder values in .env:**
```bash
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@YOUR_SERVER.postgres.database.azure.com:5432/dev_psprawls?sslmode=require
```

**Example with real values:**
```bash
DATABASE_URL=postgresql://dbadmin:MyP@ssw0rd123@mycompany-db.postgres.database.azure.com:5432/dev_psprawls?sslmode=require
```

## Step 2: Install Python Dependencies (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Setup Database (1 minute)

```bash
# Create all tables (automatically drops existing tables)
python migrate_db.py

# Add sample data
python seed_azure_db.py
```

**Note:** `migrate_db.py` always drops and recreates all tables to ensure correct schema.

## Step 4: Run Backend (30 seconds)

```bash
uvicorn main:app --host 0.0.0.0 --port 7006 --reload
```

**Test it:** Open http://localhost:7006/docs in your browser

## Step 5: Run Frontend (1 minute)

**Open a NEW terminal:**

```bash
cd frontend
npm install
npm run dev
```

**Access the app:** Open http://localhost:5000 in your browser

---

## ✅ Success Checklist

- [ ] .env file created with Azure database URL
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database migrated and seeded
- [ ] Backend running on http://localhost:7006
- [ ] Frontend running on http://localhost:5000
- [ ] You can see sample data in the app!

---

## Troubleshooting

### "DATABASE_URL not set" error
```bash
# Check .env file exists
ls backend/.env

# Check it has DATABASE_URL
cat backend/.env | grep DATABASE_URL

# Make sure you're in backend directory when running scripts
cd backend
```

### "Column does not exist" error
```bash
# Recreate tables with correct schema
cd backend
python migrate_db.py
python seed_azure_db.py
```

### "Module not found" error
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## That's It! 🎉

For more detailed instructions, see:
- `backend/SETUP_LOCAL.md` - Complete local setup guide
- `AZURE_DEV_SETUP.md` - Azure deployment guide
- `backend/README.md` - Database scripts reference
