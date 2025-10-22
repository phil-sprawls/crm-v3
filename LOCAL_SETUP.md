# Local Setup Guide - IT Platform CRM

This guide will help you publish your Replit project to GitHub and run it locally on your laptop.

## Part 1: Publishing to GitHub from Replit

### Step 1: Open the Git Pane in Replit
1. In your Replit workspace, click the **+** button in the left sidebar
2. Search for "Git" and open the Git pane

### Step 2: Initialize Git Repository
1. In the Git pane, click "Initialize repository" if not already initialized
2. You should see all your project files ready to be committed

### Step 3: Connect to GitHub
1. In the Git pane, click on "Connect to GitHub"
2. Authorize Replit to access your GitHub account
3. Choose to create a new repository or connect to an existing one
4. Name your repository (e.g., "it-platform-crm")
5. Choose whether to make it public or private

### Step 4: Commit and Push
1. Review the files in the Git pane
2. All files should be staged automatically
3. Write a commit message (e.g., "Initial commit - IT Platform CRM")
4. Click "Commit & Push" to publish to GitHub

Your code is now on GitHub! 🎉

---

## Part 2: Running Locally on Your Laptop

### Prerequisites
Install the following on your laptop:
- **Python 3.11+** - [Download from python.org](https://www.python.org/downloads/)
- **Node.js 20+** - [Download from nodejs.org](https://nodejs.org/)
- **PostgreSQL** - [Download from postgresql.org](https://www.postgresql.org/download/)
- **Git** - [Download from git-scm.com](https://git-scm.com/)

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
git clone https://github.com/YOUR_USERNAME/it-platform-crm.git
cd it-platform-crm
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Set Up PostgreSQL Database

1. **Start PostgreSQL** on your machine
2. **Create a database**:

```bash
# On Mac/Linux
psql postgres
CREATE DATABASE dev_psprawls;
\q

# On Windows (using Command Prompt)
psql -U postgres
CREATE DATABASE dev_psprawls;
\q
```

3. **Note your connection string** (you'll need it in Step 4):
   - Format: `postgresql://username:password@localhost:5432/dev_psprawls`
   - Example: `postgresql://postgres:yourpassword@localhost:5432/dev_psprawls`

### Step 3: Set Up Backend (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy the template file and fill in your database connection:

```bash
# In the backend directory
cp .env.template .env
```

Then edit `backend/.env` with your database connection:

```bash
# backend/.env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/dev_psprawls
USE_SAMPLE_DATA=false
```

Replace `yourpassword` with your PostgreSQL password.

### Step 5: Initialize Database with Sample Data

The application will automatically create tables and populate sample data on first run.

**⚠️ IMPORTANT: If you previously ran this application with an older database schema, see the [Database Migration section](#database-migration-for-existing-users) below before starting the server.**

### Step 6: Start the Backend Server

```bash
# Make sure you're in the backend directory and venv is activated
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal window open!

### Step 7: Set Up Frontend (React + Vite)

Open a **new terminal window/tab** and run:

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

You should see:
```
VITE ready in XXX ms
Local: http://localhost:5000/
```

### Step 8: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:5000
- **API Documentation**: http://localhost:8000/docs

🎉 Your CRM is now running locally!

---

## Project Structure

```
it-platform-crm/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── database.py          # Database connection
│   ├── sample_data.py       # Sample data
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (create this)
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── lib/             # API client
│   │   └── types/           # TypeScript types
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite configuration
└── LOCAL_SETUP.md           # This file
```

---

## Development Workflow

### Running Both Servers

You'll need **two terminal windows**:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Making Changes

1. **Backend changes**: The server auto-reloads when you save Python files
2. **Frontend changes**: Vite hot-reloads automatically when you save files
3. **Database changes**: Modify `models.py` and restart the backend server

---

## Common Issues & Solutions

### Issue: "Port already in use"
**Solution**: Another process is using port 8000 or 5000
```bash
# On Mac/Linux
lsof -ti:8000 | xargs kill -9
lsof -ti:5000 | xargs kill -9

# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Issue: "Database connection failed"
**Solution**: 
1. Make sure PostgreSQL is running
2. Check your DATABASE_URL in `.env` file
3. Verify the database exists: `psql -l`

### Issue: "Module not found"
**Solution**:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Issue: pip install -r requirements.txt fails
This is a common issue! Here are solutions by platform:

**Solution 1: Update pip first**
```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Then try installing again
pip install -r requirements.txt
```

**Solution 2: Install packages one by one to identify the problem**
```bash
pip install fastapi
pip install uvicorn[standard]
pip install sqlmodel
pip install psycopg2-binary
pip install python-dotenv
pip install pydantic
pip install pydantic-settings
pip install httpx
pip install pytest
```

**Solution 3: Platform-specific fixes**

**On Windows:**
- **watchfiles/uvicorn issue**: If you get "building wheel for watchfiles" error:
  ```bash
  pip install uvicorn  # WITHOUT [standard]
  ```
  Then update requirements.txt to use `uvicorn==0.24.0` instead of `uvicorn[standard]==0.24.0`

- If `psycopg2-binary` fails, you may need Visual C++ Build Tools
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or try: `pip install psycopg2-binary --only-binary :all:`

**On Mac (M1/M2/M3):**
- If `psycopg2-binary` fails:
```bash
brew install postgresql
pip install psycopg2-binary
```

**On Linux:**
- If `psycopg2-binary` fails, install PostgreSQL dev packages:
```bash
# Ubuntu/Debian
sudo apt-get install libpq-dev python3-dev

# Fedora/RHEL
sudo yum install postgresql-devel python3-devel

# Then install requirements
pip install -r requirements.txt
```

**Solution 4: Use alternative packages (if psycopg2-binary still fails)**
Edit `requirements.txt` and replace `psycopg2-binary` with `psycopg2`:
```
psycopg2==2.9.9
```

**Solution 5: Create a fresh virtual environment**
```bash
# Delete old venv
rm -rf venv  # or rmdir /s venv on Windows

# Create new one
python -m venv venv

# Activate it
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Solution 6: Check Python version**
```bash
python --version
```
Make sure it's Python 3.11 or higher. If not, install the correct version.

### Issue: Frontend can't connect to backend
**Solution**: Make sure the backend is running on port 8000 and check `frontend/src/lib/api.ts`

---

## Database Migration for Existing Users

**If you previously ran this application and now have new features (like the Intake Request system), your database schema is outdated.** The new version includes three additional tables:
- `intake_requests` - User-submitted platform assistance requests
- `request_states` - Customizable workflow states (New, In Review, Assigned, etc.)
- `request_state_assignments` - Many-to-many relationship between requests and states

### Option 1: Fresh Start (Recommended - Easiest)

**This deletes all existing data and creates a fresh database with sample data.**

```bash
# Stop the backend server (Ctrl+C if running)

# Drop and recreate the database
psql postgres
DROP DATABASE dev_psprawls;
CREATE DATABASE dev_psprawls;
\q

# Start the backend server - it will recreate all tables with sample data
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The application will automatically:
- Create all tables (including new intake request tables)
- Populate with sample data
- Set up default request states

### Option 2: Manual Migration (Keep Existing Data)

**Use this if you have important data you want to preserve.**

#### Method A: Using Python Script (Recommended - No psql needed!)

```bash
# Make sure you're in the backend directory and venv is activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the migration script
python migrate_db.py
```

The script will:
- ✅ Create all 8 database tables (if they don't exist)
- ✅ Insert 7 default request states
- ✅ Safe to run multiple times (uses IF NOT EXISTS)
- ✅ Keep all your existing data

Then start the backend server normally.

#### Method B: Using psql (If you have PostgreSQL client installed)

```bash
# Connect to your database
psql postgresql://postgres:yourpassword@localhost:5432/dev_psprawls

# Create the new tables manually
CREATE TABLE request_states (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR,
    color VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE intake_requests (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    functional_area VARCHAR NOT NULL,
    submitter_name VARCHAR NOT NULL,
    submitter_email VARCHAR NOT NULL,
    has_it_partner BOOLEAN NOT NULL,
    it_partner_name VARCHAR,
    it_partner_email VARCHAR,
    selected_help_types TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE request_state_assignments (
    id SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL REFERENCES intake_requests(id) ON DELETE CASCADE,
    state_id INTEGER NOT NULL REFERENCES request_states(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by VARCHAR,
    notes TEXT,
    UNIQUE(request_id, state_id)
);

# Insert default request states
INSERT INTO request_states (name, description, color, display_order) VALUES
    ('New', 'Request has been submitted and is awaiting review', '#3b82f6', 1),
    ('In Review', 'Request is being reviewed by the team', '#8b5cf6', 2),
    ('Assigned', 'Request has been assigned to a team member', '#0ea5e9', 3),
    ('In Progress', 'Work on the request has started', '#f59e0b', 4),
    ('Blocked', 'Request is blocked and cannot proceed', '#ef4444', 5),
    ('Completed', 'Request has been successfully completed', '#10b981', 6),
    ('Rejected', 'Request has been rejected', '#6b7280', 7);

\q
```

Then start the backend server normally.

### Option 3: Use Sample Data Mode (Testing Only)

**For testing without a database:**

Edit `backend/.env`:
```bash
USE_SAMPLE_DATA=true
# DATABASE_URL not needed in this mode
```

This runs the app with in-memory sample data (resets on restart).

### Verifying the Migration

After migration, test the new features:

1. **Start the servers** (backend and frontend)
2. **Visit the app**: http://localhost:5000
3. **Test intake requests**:
   - Navigate to "Submit Request" in the menu
   - Fill out and submit a test request
   - Navigate to "Intake Triage" (admin view) to see the request
4. **Test state management**:
   - Go to Admin → Admin States
   - View/edit the default states

**Check database tables:**
```bash
psql postgresql://postgres:yourpassword@localhost:5432/dev_psprawls

# List all tables
\dt

# Should show:
# - accounts
# - use_cases
# - updates
# - platforms
# - primary_it_partner
# - intake_requests (NEW)
# - request_states (NEW)
# - request_state_assignments (NEW)

# Check sample intake requests
SELECT * FROM intake_requests;

# Check default states
SELECT * FROM request_states ORDER BY display_order;

\q
```

---

## Stopping the Application

1. Press `Ctrl+C` in both terminal windows
2. Deactivate the Python virtual environment: `deactivate`

---

## Next Steps

- **Testing**: Run `pytest` in the backend directory
- **Building for Production**: See `replit.md` for deployment instructions
- **Database Migrations**: Consider adding Alembic for database migrations

---

## Need Help?

- Check the main `replit.md` file for architecture details
- Review the FastAPI docs at the running backend: http://localhost:8000/docs
- Check browser console for frontend errors (F12)

Happy coding! 🚀
