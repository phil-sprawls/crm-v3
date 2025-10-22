# IT Platform CRM Application

## Overview
A lightweight CRM built with FastAPI and React to manage IT team onboarding across Databricks, Snowflake, Power Platform, and Fabric. The application helps track team adoption, use cases, updates, and health status for internal platform onboarding.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM with Pydantic validation
- **Pydantic** - Data validation and settings management
- **PostgreSQL** - Relational database (Replit-provided or Azure PostgreSQL)
- **Uvicorn** - ASGI server
- **Pytest** - Testing framework

### Frontend
- **React 18+** - UI library with TypeScript
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS v3** - Utility-first CSS framework
- **shadcn/UI** - Component library patterns
- **Axios** - HTTP client
- **Playwright** - E2E testing framework

## Project Structure

```
workspace/
├── backend/
│   ├── models.py          # SQLModel database models
│   ├── database.py        # Database connection and session management
│   ├── main.py            # FastAPI application with all API endpoints
│   ├── sample_data.py     # Sample data for initial population
│   └── test_main.py       # Pytest test suite
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components (AllAccounts, AccountDetails, Admin)
│   │   ├── lib/           # Utilities and API client
│   │   ├── types/         # TypeScript type definitions
│   │   ├── App.tsx        # Main app component with routing
│   │   ├── main.tsx       # React entry point
│   │   └── index.css      # Global styles with Tailwind
│   ├── vite.config.ts     # Vite configuration
│   ├── tsconfig.json      # TypeScript configuration
│   └── playwright.config.ts # Playwright test configuration
└── package.json           # Node.js dependencies and scripts
```

## Database Schema

### Tables
1. **Accounts** - Main account/team information
   - UID (Primary Key), Team, Business/IT Area, VP, Team Admin
   - Use Case, Use Case Status, Platform onboarding status
   - Tech stack, AD groups, Git repo, ADO items
   - CSM, Health, Health Reason

2. **Use_Cases** - Use cases for each account
   - Problem, Solution, Value, Leader, Status
   - Enablement Tier, Platform

3. **Updates** - Activity updates for accounts
   - Description, Author, Platform, Date

4. **Platforms** - Platform onboarding status
   - Platform Name (Databricks, Snowflake, Power Platform, Fabric)
   - Onboarding Status

5. **Primary_IT_Partner** - IT partner assignments
   - Primary IT Partner name per account

## Features

### All Accounts Screen
- Displays searchable table of all accounts
- Search by Team, Business/IT Area, VP, or Admin
- View button to navigate to account details

### Account Details Screen
- Comprehensive view of account information
- Related platforms, use cases, updates
- Primary IT Partner information
- Health status with color coding (Green/Yellow/Red)

### Admin Screen
- Update account health (CSM, Health, Health Reason)
- Add new use cases
- Add updates
- Add platform onboarding records

### Dark Mode Support
- Built-in theme toggle
- Persistent theme preference (localStorage)
- Full dark mode styling across all components

## Running the Application

### Development (Replit)
The workflow automatically runs both backend and frontend:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:5000
- API Documentation: http://localhost:8000/docs

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (auto-configured in Replit)
- `USE_SAMPLE_DATA` - Set to "true" for in-memory sample data mode (default: false)
- `ADMIN_EMAIL` - Email address to receive intake request notifications (optional)
- `AZURE_COMMUNICATION_CONNECTION_STRING` - Azure Communication Services connection string for email (optional)

### Sample Data
On first startup, the application automatically populates the database with sample accounts, use cases, updates, platforms, and IT partners.

## API Endpoints

### Accounts
- `GET /api/accounts` - List all accounts
- `GET /api/accounts/{uid}` - Get account by UID
- `POST /api/accounts` - Create new account
- `PUT /api/accounts/{uid}` - Update account
- `DELETE /api/accounts/{uid}` - Delete account

### Related Data
- `GET /api/accounts/{uid}/use-cases` - Get account use cases
- `GET /api/accounts/{uid}/updates` - Get account updates
- `GET /api/accounts/{uid}/platforms` - Get account platforms
- `GET /api/accounts/{uid}/primary-it-partner` - Get primary IT partner

### CRUD Operations
- Use Cases: POST/PUT/DELETE `/api/use-cases`
- Updates: POST/PUT/DELETE `/api/updates`
- Platforms: POST/PUT/DELETE `/api/platforms`
- IT Partners: POST/PUT/DELETE `/api/primary-it-partners`

## Testing

### Backend Tests
```bash
cd backend && pytest
```

### Frontend E2E Tests
```bash
cd frontend && npx playwright test
```

## Deployment to Azure

### Minimal Changes Required

1. **Database Connection**
   - Update `DATABASE_URL` environment variable to Azure PostgreSQL connection string
   - No code changes needed

2. **Azure JWT Authentication**
   - Add Azure AD middleware to `backend/main.py`
   - Configure CORS for Azure domain
   - Authentication structure is ready for JWT token validation

3. **Docker Configuration** (Add these files)
   ```dockerfile
   # backend/Dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY backend/ .
   RUN pip install -r requirements.txt
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   
   # frontend/Dockerfile
   FROM node:20-alpine
   WORKDIR /app
   COPY frontend/ .
   RUN npm install && npm run build
   CMD ["npm", "run", "preview"]
   ```

4. **Docker Compose**
   ```yaml
   version: '3.8'
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=${DATABASE_URL}
     frontend:
       build: ./frontend
       ports:
         - "5000:5000"
   ```

5. **Kubernetes Manifests**
   - Add deployment.yaml and service.yaml for both frontend and backend
   - Configure ingress for routing

6. **GitHub Actions CI/CD**
   ```yaml
   # .github/workflows/deploy.yml
   name: Deploy to Azure
   on:
     push:
       branches: [main]
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Build and push Docker images
         - name: Deploy to AKS
   ```

## Architecture Notes

### Data Mode
- **Database Mode** (default): Uses PostgreSQL for persistent storage
- **Sample Data Mode**: Set `USE_SAMPLE_DATA=true` for in-memory demo data

### API Design
- RESTful API following OpenAPI 3.0 specification
- Full CRUD operations for all entities
- Foreign key relationships enforced at database level
- Comprehensive error handling with HTTP status codes

### Frontend Architecture
- Component-based React architecture
- Type-safe with TypeScript
- Client-side routing with React Router
- Centralized API client in `lib/api.ts`
- Reusable UI components following shadcn/UI patterns

## Recent Changes
- **2025-10-21**: Added intake request system
  - Created intake form with multi-select card-based UI for help types
  - Added intake triage view for admins to review and manage requests
  - Implemented request state management system with custom states
  - Added AdminStates page for creating/editing/deleting custom states
  - New database tables: intake_requests, request_states, request_state_assignments
  - Default states: New, In Review, Assigned, In Progress, Blocked, Completed, Rejected
  - Sample functional areas: Finance, Marketing, Sales, Operations, HR, IT, Product, Engineering, Customer Success, Legal, R&D, Supply Chain
  - Email notifications placeholder for Azure Communication Services (requires ADMIN_EMAIL and AZURE_COMMUNICATION_CONNECTION_STRING)
  - Navigation updated with Submit Request and Intake Triage links
  - Access control: public form submission, admin-only triage view
- **2025-10-13**: Initial application setup and deployment
  - Created PostgreSQL database with all tables (Accounts, Use_Cases, Updates, Platforms, Primary_IT_Partner)
  - Implemented FastAPI backend with full CRUD endpoints including partial update support
  - Built React frontend with TypeScript and Vite
  - Added dark mode support with persistent theme preference
  - Created All Accounts screen with search functionality
  - Created Account Details screen with comprehensive data display showing ALL account fields
  - Enhanced Account Details to display ADO links, Git repo, AD groups, team artifacts as clickable links
  - Created Admin screen for managing use cases, updates, platforms, and health status
  - **Added New Account page** with comprehensive form to create accounts with all fields
  - **Added Edit Account page** to modify all account information (UID is disabled as primary key)
  - Added "New Account" button to All Accounts page
  - Added "Edit Account" button to Account Details page
  - Added routes for /accounts/new and /accounts/:uid/edit
  - **Enhanced Admin panel with edit functionality**:
    - Added inline edit forms for platforms with Edit/Delete buttons for each platform
    - Added inline edit forms for updates with Edit/Delete buttons for each update
    - Added inline edit forms for use cases with Edit/Delete buttons for each use case
    - All sections display existing items with summary and allow editing without navigation
    - Confirmation dialogs for deletion operations
    - Automatic data refresh after edit/delete operations
  - **Improved loading experience**:
    - Account Details page shows animated spinner during data loading
    - Enhanced "Account not found" state with "Return to Accounts" button
  - **Enhanced theme toggle**:
    - Replaced moon/sun icon with settings gear icon
    - Added dropdown menu with Light, Dark, and System theme options
    - System option respects and follows OS theme preference
    - Theme selection persists in localStorage with visual checkmarks
    - Default theme set to System for automatic OS preference matching
  - Implemented AccountUpdate schemas with optional fields for partial updates
  - Added manual cascade deletion for accounts to handle related records
  - Fixed API URL configuration to work in Replit environment
  - Populated sample data for three demo accounts with full relationships
  - Successfully deployed and verified all functionality

## Running Locally

See **LOCAL_SETUP.md** for complete instructions on:
- Publishing this project to GitHub from Replit
- Setting up the development environment on your laptop
- Running the backend (Python/FastAPI) and frontend (React/Vite) locally
- **Database migration for existing users** - If you previously ran this app locally, you'll need to update your database schema to include the new intake request tables
- Troubleshooting common issues

## Azure Development Environment Setup

See **AZURE_DEV_SETUP.md** for complete instructions on:
- Creating environment configuration files (.env)
- Setting up Azure PostgreSQL Flexible Server
- Seeding Azure database with sample data using Python script
- Deploying backend (FastAPI) to Azure App Service (existing or new)
- Configuring Azure AD authentication with JWT tokens (optional)
- Deploying frontend (React) to Azure App Service
- Environment variables summary (required and optional)
- Monitoring and troubleshooting
- Cost estimation (~$28/month for dev environment)

## User Preferences
- Clean, modern UI design with Tailwind CSS
- Dark mode support for better accessibility
- Searchable data tables for easy navigation
- Comprehensive admin panel for data management
