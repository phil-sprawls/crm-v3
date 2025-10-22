# Azure Development Environment Setup Guide

Complete guide to set up your IT Platform CRM development environment on Azure.

---

## 📋 Prerequisites

- **Azure CLI** installed ([Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- **Azure PostgreSQL Database** (existing or new)
- **Azure Subscription** with contributor access
- **Python 3.11+** installed locally
- **Node.js 20+** installed locally

---

## 🚀 Quick Setup Overview

1. Create environment configuration file
2. Set up Azure PostgreSQL database
3. Seed database with sample data
4. Deploy backend to Azure App Service
5. Configure JWT authentication (optional)
6. Deploy frontend to Azure App Service
7. Test your application

---

## Step 1: Create Environment Configuration File

Copy the template file and fill in your values:

```bash
# Navigate to backend directory
cd backend

# Copy template to create your .env file
cp .env.template .env

# Edit the file with your actual values
# (Use your preferred text editor)
```

### Local Development `.env`

Example configuration for local development:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/dev_psprawls
USE_SAMPLE_DATA=false

# Azure AD Authentication (Optional - for JWT)
APP_CLIENT_ID=your-azure-ad-app-client-id
TENANT_ID=your-azure-tenant-id
OPENAPI_CLIENT_ID=your-openapi-client-id

# Email Notifications (Optional)
ADMIN_EMAIL=admin@yourcompany.com
AZURE_COMMUNICATION_CONNECTION_STRING=your-azure-communication-services-connection-string

# Environment
ENVIRONMENT=development
```

### Azure Production `.env` Variables

For Azure App Service, set these as **Application Settings**:

```bash
# Required
DATABASE_URL=postgresql://username:password@server.postgres.database.azure.com:5432/dev_psprawls?sslmode=require
USE_SAMPLE_DATA=false

# Optional - JWT Authentication
APP_CLIENT_ID=<your-app-client-id>
TENANT_ID=<your-tenant-id>
OPENAPI_CLIENT_ID=<your-openapi-client-id>

# Optional - Email Notifications
ADMIN_EMAIL=admin@yourcompany.com
AZURE_COMMUNICATION_CONNECTION_STRING=<connection-string>

# Required for Azure
SCM_DO_BUILD_DURING_DEPLOYMENT=true
ENVIRONMENT=production
```

---

## Step 2: Set Up Azure PostgreSQL Database

### Option A: Use Existing Database

If you already have an Azure PostgreSQL database, get your connection details:

```bash
# List your PostgreSQL servers
az postgres flexible-server list --output table

# Get connection info
az postgres flexible-server show \
  --resource-group YOUR_RESOURCE_GROUP \
  --name YOUR_SERVER_NAME
```

**Connection String Format:**
```
postgresql://USERNAME:PASSWORD@SERVER.postgres.database.azure.com:5432/DATABASE?sslmode=require
```

### Option B: Create New Database

```bash
# Set variables
RESOURCE_GROUP="crm-dev-rg"
LOCATION="eastus"
SERVER_NAME="crm-db-dev-$(date +%s)"  # Adds timestamp for uniqueness
ADMIN_USER="crmadmin"
ADMIN_PASSWORD="YourSecurePassword123!"  # Change this!
DATABASE_NAME="dev_psprawls"

# Create resource group (if needed)
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create PostgreSQL Flexible Server
az postgres flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $SERVER_NAME \
  --location $LOCATION \
  --admin-user $ADMIN_USER \
  --admin-password $ADMIN_PASSWORD \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 14

# Create database
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $SERVER_NAME \
  --database-name $DATABASE_NAME

# Allow Azure services access
az postgres flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $SERVER_NAME \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Allow your IP (for local development)
MY_IP=$(curl -s https://api.ipify.org)
az postgres flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $SERVER_NAME \
  --rule-name AllowMyIP \
  --start-ip-address $MY_IP \
  --end-ip-address $MY_IP

# Build connection string
DATABASE_URL="postgresql://${ADMIN_USER}:${ADMIN_PASSWORD}@${SERVER_NAME}.postgres.database.azure.com:5432/${DATABASE_NAME}?sslmode=require"
echo "Your DATABASE_URL: $DATABASE_URL"
```

---

## Step 3: Initialize and Seed Database

### 3a. Create Tables (Migration)

Run the migration script to create all database tables:

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if using one)
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Set your Azure DATABASE_URL in .env file
echo "DATABASE_URL=your-azure-connection-string" >> .env

# Run migration
python migrate_db.py
```

Expected output:
```
============================================================
Database Migration - Create All Tables
============================================================
🔌 Connecting to database...
✅ Connected successfully
📋 Creating accounts table...
✅ accounts table created
📋 Creating use_cases table...
✅ use_cases table created
📋 Creating updates table...
✅ updates table created
📋 Creating platforms_crm table...
✅ platforms_crm table created
📋 Creating primary_it_partners table...
✅ primary_it_partners table created
📋 Creating request_states table...
✅ request_states table created
📋 Creating intake_requests table...
✅ intake_requests table created
📋 Creating request_state_assignments table...
✅ request_state_assignments table created
🔍 Checking for existing states...
📝 Inserting default request states...
✅ Default states inserted
🎉 Migration completed successfully!

All tables created:
  - accounts
  - use_cases
  - updates
  - platforms_crm
  - primary_it_partners
  - request_states
  - intake_requests
  - request_state_assignments
```

### 3b. Seed with Sample Data

Run the seeding script to populate with sample data:

```bash
# Make sure DATABASE_URL is set in .env
python seed_azure_db.py
```

Expected output:
```
============================================================
Azure Database Seeding Script
============================================================
🔌 Connecting to Azure PostgreSQL database...
✅ Connected successfully
📝 Inserting sample accounts...
✅ Sample accounts inserted
...
🎉 Database seeding completed successfully!

Sample data created:
  - 3 Accounts (ACC001, ACC002, ACC003)
  - 3 Use Cases
  - 3 Updates
  - 6 Platform records
  - 3 IT Partners
  - 7 Request States
  - 2 Intake Requests
```

---

## Step 4: Deploy Backend to Azure App Service

### Option A: Deploy to Existing App Service

```bash
# Login to Azure
az login

# Set variables
RESOURCE_GROUP="your-resource-group"
BACKEND_APP_NAME="your-existing-app-service"
DATABASE_URL="your-postgresql-connection-string"

# Update environment variables
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --settings \
    DATABASE_URL="$DATABASE_URL" \
    USE_SAMPLE_DATA="false" \
    ENVIRONMENT="production" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# Update startup command
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"

# Deploy code
cd backend
zip -r backend.zip . -x "*.pyc" -x "__pycache__/*" -x "venv/*" -x ".env"
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --src backend.zip

echo "✅ Backend deployed to: https://${BACKEND_APP_NAME}.azurewebsites.net"
```

### Option B: Create New App Service

```bash
# Set variables
RESOURCE_GROUP="crm-dev-rg"
BACKEND_APP_NAME="crm-backend-dev-$(date +%s)"  # Unique name
DATABASE_URL="your-postgresql-connection-string"

# Create App Service Plan (Linux, B1 tier)
az appservice plan create \
  --name crm-dev-plan \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan crm-dev-plan \
  --name $BACKEND_APP_NAME \
  --runtime "PYTHON:3.11"

# Configure environment variables
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --settings \
    DATABASE_URL="$DATABASE_URL" \
    USE_SAMPLE_DATA="false" \
    ENVIRONMENT="production" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# Set startup command
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"

# Deploy code
cd backend
zip -r backend.zip . -x "*.pyc" -x "__pycache__/*" -x "venv/*" -x ".env"
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --src backend.zip

echo "✅ Backend deployed to: https://${BACKEND_APP_NAME}.azurewebsites.net"
```

### Test Backend

```bash
# Test API endpoint
curl https://${BACKEND_APP_NAME}.azurewebsites.net/api/accounts

# View API documentation
open https://${BACKEND_APP_NAME}.azurewebsites.net/docs
```

---

## Step 5: Configure JWT Authentication (Optional)

If you want to secure your API with Azure AD authentication:

### 5a. Register Application in Azure AD

```bash
# Create App Registration for API
az ad app create \
  --display-name "CRM Backend API" \
  --sign-in-audience AzureADMyOrg \
  --enable-id-token-issuance true \
  --query appId -o tsv

# Save the output as APP_CLIENT_ID
APP_CLIENT_ID="<output-from-above>"
TENANT_ID=$(az account show --query tenantId -o tsv)

echo "APP_CLIENT_ID: $APP_CLIENT_ID"
echo "TENANT_ID: $TENANT_ID"
```

### 5b. Create OpenAPI App Registration

For interactive API documentation:

```bash
# Create App Registration for OpenAPI UI
az ad app create \
  --display-name "CRM Backend API - OpenAPI" \
  --sign-in-audience AzureADMyOrg \
  --web-redirect-uris "https://${BACKEND_APP_NAME}.azurewebsites.net/oauth2-redirect" \
  --enable-id-token-issuance true \
  --query appId -o tsv

# Save as OPENAPI_CLIENT_ID
OPENAPI_CLIENT_ID="<output-from-above>"
echo "OPENAPI_CLIENT_ID: $OPENAPI_CLIENT_ID"
```

### 5c. Configure API Permissions

Via Azure Portal:
1. Go to **Azure Active Directory** → **App Registrations**
2. Find your "CRM Backend API" registration
3. Click **Expose an API** → **Add a scope**
4. Scope name: `user_impersonation`
5. Consent: "Admins and users"
6. Save

Then for OpenAPI app:
1. Find "CRM Backend API - OpenAPI" registration
2. Click **API permissions** → **Add a permission** → **My APIs**
3. Select "CRM Backend API" → Check `user_impersonation`
4. Click **Grant admin consent**

### 5d. Add JWT Environment Variables to Azure

```bash
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --settings \
    APP_CLIENT_ID="$APP_CLIENT_ID" \
    TENANT_ID="$TENANT_ID" \
    OPENAPI_CLIENT_ID="$OPENAPI_CLIENT_ID"
```

### 5e. Install fastapi-azure-auth

Add to `backend/requirements.txt`:
```
fastapi-azure-auth==4.3.1
```

Redeploy your backend after adding the dependency.

---

## Step 6: Deploy Frontend to Azure

### 6a. Update Frontend API URL

Edit `frontend/src/lib/api.ts` to include your backend URL:

```typescript
const getApiBaseUrl = () => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  if (hostname.includes('replit.dev')) {
    return `${protocol}//${hostname}:8000`;
  }
  
  if (hostname.includes('azurewebsites.net')) {
    return 'https://your-backend-name.azurewebsites.net';  // ← UPDATE THIS
  }
  
  return 'http://localhost:8000';
};
```

### 6b. Update Backend CORS

Edit `backend/main.py` to allow your frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "https://your-frontend-name.azurewebsites.net",  # ← ADD YOUR FRONTEND URL
        "*"  # Remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6c. Build and Deploy Frontend

```bash
# Set variables
FRONTEND_APP_NAME="crm-frontend-dev-$(date +%s)"  # Unique name

# Build frontend
cd frontend
npm install
npm run build

# Create App Service
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan crm-dev-plan \
  --name $FRONTEND_APP_NAME \
  --runtime "NODE:20-lts"

# Configure startup (static file serving)
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $FRONTEND_APP_NAME \
  --startup-file "npx serve -s dist -l 8080"

# Deploy
zip -r frontend.zip dist/ package.json package-lock.json
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $FRONTEND_APP_NAME \
  --src frontend.zip

echo "✅ Frontend deployed to: https://${FRONTEND_APP_NAME}.azurewebsites.net"
```

---

## Step 7: Test Your Application

### Backend Tests

```bash
# Test API
curl https://${BACKEND_APP_NAME}.azurewebsites.net/api/accounts

# Expected: JSON array with 3 sample accounts

# Test specific account
curl https://${BACKEND_APP_NAME}.azurewebsites.net/api/accounts/ACC001

# Test intake requests
curl https://${BACKEND_APP_NAME}.azurewebsites.net/api/intake-requests

# View API docs
open https://${BACKEND_APP_NAME}.azurewebsites.net/docs
```

### Frontend Tests

Open your frontend URL in a browser:
```bash
open https://${FRONTEND_APP_NAME}.azurewebsites.net
```

**Test these features:**
1. **All Accounts** - Should show 3 sample accounts
2. **Submit Request** - Submit a test request
3. **Intake Triage** - View submitted requests (should see 2 sample requests)
4. **Admin States** - View/manage the 7 default workflow states
5. **Account Details** - Click "View" on any account
6. **Admin Panel** - Add use cases, updates, platforms

---

## 🔍 Troubleshooting

### View Backend Logs

```bash
# Stream live logs
az webapp log tail \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME

# Download logs
az webapp log download \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --log-file backend-logs.zip
```

### Common Issues

**Database Connection Failed**
- ✅ Check firewall rules allow Azure services (0.0.0.0-0.0.0.0)
- ✅ Verify DATABASE_URL format includes `?sslmode=require`
- ✅ Test connection locally: `psql "your-connection-string"`

**Application Error / 500**
- ✅ Check logs: `az webapp log tail`
- ✅ Verify all environment variables are set
- ✅ Check startup command is correct

**CORS Errors**
- ✅ Add frontend URL to CORS allowed origins in `main.py`
- ✅ Redeploy backend after CORS changes
- ✅ Clear browser cache

**Frontend Can't Connect to Backend**
- ✅ Verify API URL in `frontend/src/lib/api.ts`
- ✅ Check backend is running: `curl backend-url/api/accounts`
- ✅ Check browser console for errors (F12)

---

## 📊 Environment Variables Summary

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@server.postgres.database.azure.com:5432/db?sslmode=require` |
| `USE_SAMPLE_DATA` | Use in-memory data (development only) | `false` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | Enable build on Azure | `true` |

### Optional Variables (JWT Authentication)

| Variable | Description | How to Get |
|----------|-------------|-----------|
| `APP_CLIENT_ID` | Azure AD App Client ID | `az ad app create --display-name "CRM API"` |
| `TENANT_ID` | Azure Tenant ID | `az account show --query tenantId` |
| `OPENAPI_CLIENT_ID` | OpenAPI UI Client ID | Create separate App Registration |

### Optional Variables (Email)

| Variable | Description | How to Get |
|----------|-------------|-----------|
| `ADMIN_EMAIL` | Email for notifications | Your admin email address |
| `AZURE_COMMUNICATION_CONNECTION_STRING` | Azure Communication Services | Azure Portal → Communication Services |

---

## 🎯 Next Steps

### For Development
- Set up CI/CD with GitHub Actions
- Configure custom domain
- Add Application Insights for monitoring
- Set up staging environment

### For Production
- Remove CORS wildcard (`*`)
- Enable JWT authentication
- Configure SSL/TLS certificates
- Set up backup strategy for database
- Configure auto-scaling rules
- Add health check endpoints

---

## 📚 Additional Resources

- [Azure PostgreSQL Documentation](https://docs.microsoft.com/en-us/azure/postgresql/)
- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [FastAPI Azure Auth](https://github.com/Intility/fastapi-azure-auth)
- [Azure AD Authentication](https://docs.microsoft.com/en-us/azure/active-directory/develop/)

---

## 💰 Cost Estimation

**Monthly costs for development environment:**
- PostgreSQL Flexible Server (B1ms): ~$15/month
- App Service Plan (B1): ~$13/month
- **Total: ~$28/month**

**Tips to reduce costs:**
- Use Burstable tier for database
- Share App Service Plan between frontend and backend
- Stop resources when not in use
- Use Azure Dev/Test pricing if eligible
