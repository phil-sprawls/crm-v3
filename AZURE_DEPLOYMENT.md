# Azure Development Environment Deployment Guide

Complete guide to deploy the IT Platform CRM to Azure for development/testing.

---

## 🚀 Quick Start (Already Have PostgreSQL Database)

**If you already have an Azure PostgreSQL database provisioned**, follow these minimal steps:

### ℹ️ About Resource Groups

**What is a Resource Group?**  
A resource group is just an organizational container in Azure - think of it as a folder for related resources. **All Azure resources require one**, but:

✅ **You likely already have one** - Check with: `az group list --output table`  
✅ **Your PostgreSQL database is already in one** - Use the same group  
✅ **IT/DevOps may have created one** - Ask your team  
✅ **Creating one is simple** - Just one command if needed  

**Why other apps don't mention it:**  
Many apps use existing resource groups created by IT teams, or deployment tools create them automatically behind the scenes. It's not complex - just a name you need to provide.

---

### Step 1: Get Your Database Connection String

**Find which resource group your PostgreSQL database is in:**
```bash
az postgres flexible-server list --output table
# Shows: Name, ResourceGroup, Location, etc.
```

**Connection String Format:**
```
postgresql://USERNAME:PASSWORD@SERVER.postgres.database.azure.com:5432/DATABASE?sslmode=require
```

**Example:**
```
postgresql://crmadmin:MyPassword123@myserver.postgres.database.azure.com:5432/crm_db?sslmode=require
```

**Tip:** Use the same resource group as your database - keeps everything organized together!

### Step 2: Deploy Backend (5 minutes)

```bash
# Login to Azure
az login

# List your existing resource groups (you likely already have one)
az group list --output table

# Set variables - USE AN EXISTING RESOURCE GROUP or create new one
RESOURCE_GROUP="crm-dev-rg"  # ← Replace with your existing resource group name
BACKEND_APP_NAME="crm-backend-dev"  # Must be globally unique
DATABASE_URL="your-postgresql-connection-string-here"

# Only if you need a new resource group (skip if using existing)
# az group create --name $RESOURCE_GROUP --location eastus

# Create App Service Plan (if you don't have one)
# Check existing plans: az appservice plan list --output table
az appservice plan create \
  --name crm-dev-plan \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# Create Backend App Service
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
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# Set startup command
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"

# Deploy backend code
cd backend
zip -r backend.zip .
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --src backend.zip

# Get backend URL
echo "Backend URL: https://${BACKEND_APP_NAME}.azurewebsites.net"
```

### Step 3: Update Frontend API URL

Edit `frontend/src/lib/api.ts`:

```typescript
const getApiBaseUrl = () => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  if (hostname.includes('replit.dev')) {
    return `${protocol}//${hostname}:8000`;
  }
  
  if (hostname.includes('azurewebsites.net')) {
    return 'https://crm-backend-dev.azurewebsites.net';  // ← YOUR BACKEND URL
  }
  
  return 'http://localhost:8000';
};
```

### Step 4: Update Backend CORS

Edit `backend/main.py` and add your frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "https://crm-frontend-dev.azurewebsites.net",  # ← YOUR FRONTEND URL
        "*"  # Remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 5: Deploy Frontend (5 minutes)

```bash
FRONTEND_APP_NAME="crm-frontend-dev"  # Must be globally unique

# Build frontend
cd frontend
npm install
npm run build

# Create Frontend App Service
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan crm-dev-plan \
  --name $FRONTEND_APP_NAME \
  --runtime "NODE:20-lts"

# Deploy frontend
cd frontend
zip -r frontend.zip dist/
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $FRONTEND_APP_NAME \
  --src frontend.zip

# Get frontend URL
echo "Frontend URL: https://${FRONTEND_APP_NAME}.azurewebsites.net"
```

### Step 6: Test Your App

```bash
# Backend API
curl https://crm-backend-dev.azurewebsites.net/api/accounts

# Frontend
open https://crm-frontend-dev.azurewebsites.net
```

### Troubleshooting

**View backend logs:**
```bash
az webapp log tail --resource-group $RESOURCE_GROUP --name $BACKEND_APP_NAME
```

**Common issues:**
- **Database connection failed**: Check firewall rules allow Azure services (0.0.0.0-0.0.0.0)
- **Application Error**: Check logs above
- **CORS errors**: Verify frontend URL in backend CORS settings

---

## 📖 Full Deployment Guide

For complete instructions including PostgreSQL setup, Azure AD authentication, and CI/CD, see sections below.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Azure PostgreSQL Setup](#azure-postgresql-setup)
3. [Backend Deployment (FastAPI)](#backend-deployment-fastapi)
4. [Frontend Deployment (React)](#frontend-deployment-react)
5. [Azure AD Authentication](#azure-ad-authentication)
6. [Environment Configuration](#environment-configuration)
7. [CI/CD with GitHub Actions](#cicd-with-github-actions)
8. [Monitoring & Troubleshooting](#monitoring--troubleshooting)

---

## Prerequisites

### Required Tools
```bash
# Install Azure CLI
# Windows: Download from https://aka.ms/installazurecliwindows
# Mac: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify installation
az --version

# Login to Azure
az login

# Set your subscription (if you have multiple)
az account list --output table
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### Azure Resources Needed
- **Azure Subscription** (free tier works for dev)
- **Resource Group** (container for all resources)
- **App Service Plan** (hosting for frontend/backend)
- **PostgreSQL Flexible Server** (database)
- **Azure AD App Registration** (authentication)

---

## Azure PostgreSQL Setup

### Step 1: Create PostgreSQL Flexible Server

```bash
# Set variables
RESOURCE_GROUP="crm-dev-rg"
LOCATION="eastus"
PG_SERVER_NAME="crm-postgres-dev"  # Must be globally unique
ADMIN_USER="crmadmin"
ADMIN_PASSWORD="YourSecurePassword123!"  # Change this!

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Create PostgreSQL Flexible Server
az postgres flexible-server create \
  --name $PG_SERVER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --admin-user $ADMIN_USER \
  --admin-password $ADMIN_PASSWORD \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 15 \
  --public-access 0.0.0.0
```

**Note:** `--public-access 0.0.0.0` allows all Azure services. For production, use VNet integration or specific IPs.

### Step 2: Create Database

```bash
# Create the CRM database
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $PG_SERVER_NAME \
  --database-name crm_db
```

### Step 3: Configure Firewall Rules

```bash
# Allow your current IP for management
MY_IP=$(curl -s ifconfig.me)
az postgres flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $PG_SERVER_NAME \
  --rule-name AllowMyIP \
  --start-ip-address $MY_IP \
  --end-ip-address $MY_IP

# Allow Azure services (for App Service connection)
az postgres flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $PG_SERVER_NAME \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### Step 4: Get Connection String

```bash
# Your connection string will be:
DATABASE_URL="postgresql://${ADMIN_USER}:${ADMIN_PASSWORD}@${PG_SERVER_NAME}.postgres.database.azure.com:5432/crm_db?sslmode=require"

# Save this - you'll need it for backend configuration
echo $DATABASE_URL
```

**Example:**
```
postgresql://crmadmin:YourSecurePassword123!@crm-postgres-dev.postgres.database.azure.com:5432/crm_db?sslmode=require
```

---

## Backend Deployment (FastAPI)

### Step 1: Prepare Backend for Azure

Create `backend/startup.sh`:

```bash
#!/bin/bash
# Azure uses Gunicorn with Uvicorn workers for FastAPI
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 600 main:app
```

Make it executable:
```bash
chmod +x backend/startup.sh
```

### Step 2: Update requirements.txt

Add Gunicorn to `backend/requirements.txt`:

```txt
fastapi==0.104.1
uvicorn==0.24.0
gunicorn==21.2.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.2
pytest==7.4.3
```

### Step 3: Create App Service Plan

```bash
# Create Linux App Service Plan (B1 tier for dev)
az appservice plan create \
  --name crm-dev-plan \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku B1 \
  --is-linux
```

**Pricing Tiers:**
- **Free (F1)**: $0/month, shared CPU, 1GB RAM, 60min/day limit
- **Basic (B1)**: ~$13/month, 1 vCPU, 1.75GB RAM (recommended for dev)
- **Standard (S1)**: ~$70/month, better for production

### Step 4: Create Backend App Service

```bash
BACKEND_APP_NAME="crm-backend-dev"  # Must be globally unique

az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan crm-dev-plan \
  --name $BACKEND_APP_NAME \
  --runtime "PYTHON:3.11" \
  --deployment-local-git
```

### Step 5: Configure Backend Environment Variables

```bash
# Set environment variables
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --settings \
    DATABASE_URL="$DATABASE_URL" \
    USE_SAMPLE_DATA="false" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"
```

### Step 6: Set Startup Command

```bash
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"
```

### Step 7: Deploy Backend

**Option A: Local Git Deployment**

```bash
# Get deployment credentials
az webapp deployment list-publishing-credentials \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --query "{username:publishingUserName, password:publishingPassword}" \
  --output table

# Add Azure remote
cd backend
git init
git add .
git commit -m "Initial backend deployment"
git remote add azure $(az webapp deployment source config-local-git \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query url --output tsv)

# Push to Azure (enter credentials when prompted)
git push azure main
```

**Option B: ZIP Deployment (Easier)**

```bash
cd backend
zip -r backend.zip .
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --src backend.zip
```

### Step 8: Verify Backend

```bash
# Get backend URL
BACKEND_URL="https://${BACKEND_APP_NAME}.azurewebsites.net"
echo $BACKEND_URL

# Test the API
curl $BACKEND_URL/api/accounts

# View logs
az webapp log tail --resource-group $RESOURCE_GROUP --name $BACKEND_APP_NAME
```

---

## Frontend Deployment (React)

### Step 1: Update API URL for Azure

Edit `frontend/src/lib/api.ts`:

```typescript
const getApiBaseUrl = () => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  // Check if running on Replit
  if (hostname.includes('replit.dev')) {
    return `${protocol}//${hostname}:8000`;
  }
  
  // Check if running on Azure
  if (hostname.includes('azurewebsites.net')) {
    return 'https://crm-backend-dev.azurewebsites.net';  // Update with your backend URL
  }
  
  // Local development
  return 'http://localhost:8000';
};
```

### Step 2: Update CORS in Backend

Edit `backend/main.py` to allow Azure frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "https://crm-frontend-dev.azurewebsites.net",  # Your frontend URL
        "*"  # Remove this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 3: Build React App

```bash
cd frontend
npm install
npm run build
```

This creates a `dist/` folder with optimized production files.

### Step 4: Create Frontend App Service

```bash
FRONTEND_APP_NAME="crm-frontend-dev"  # Must be globally unique

az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan crm-dev-plan \
  --name $FRONTEND_APP_NAME \
  --runtime "NODE:20-lts"
```

### Step 5: Configure Frontend for SPA

```bash
# Create routes configuration for client-side routing
cat > frontend/staticwebapp.config.json << 'EOF'
{
  "navigationFallback": {
    "rewrite": "/index.html"
  }
}
EOF
```

### Step 6: Deploy Frontend

```bash
cd frontend
zip -r frontend.zip dist/

az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $FRONTEND_APP_NAME \
  --src frontend.zip
```

### Step 7: Verify Frontend

```bash
FRONTEND_URL="https://${FRONTEND_APP_NAME}.azurewebsites.net"
echo $FRONTEND_URL

# Open in browser
open $FRONTEND_URL  # Mac
start $FRONTEND_URL  # Windows
```

---

## Azure AD Authentication

### Step 1: Register Application in Azure AD

```bash
# Create App Registration
az ad app create \
  --display-name "CRM Backend API" \
  --sign-in-audience AzureADMyOrg \
  --enable-id-token-issuance true \
  --query appId -o tsv

# Save the App ID (Client ID)
APP_CLIENT_ID="<output-from-above>"
TENANT_ID=$(az account show --query tenantId -o tsv)
```

**Or via Azure Portal:**
1. Go to **Azure Active Directory** → **App Registrations** → **New Registration**
2. Name: "CRM Backend API"
3. Supported account types: "Accounts in this organizational directory only"
4. Click **Register**
5. Copy **Application (client) ID** and **Directory (tenant) ID**

### Step 2: Expose API Scope

In Azure Portal:
1. Go to your App Registration
2. Click **Expose an API**
3. Click **Add a scope**
4. Application ID URI: `api://{APP_CLIENT_ID}`
5. Scope name: `user_impersonation`
6. Who can consent: "Admins and users"
7. Fill in display names and descriptions
8. Click **Add scope**

### Step 3: Create OpenAPI/Swagger App Registration

For interactive API docs:
1. Create another App Registration: "CRM Backend API - OpenAPI"
2. Copy the Client ID
3. Under **Authentication** → **Add Platform** → **Single-page application**
4. Redirect URI: `https://crm-backend-dev.azurewebsites.net/oauth2-redirect`
5. Under **API Permissions** → **Add permission** → **My APIs**
6. Select "CRM Backend API" → Check `user_impersonation` → **Add permissions**

### Step 4: Install Azure AD Library

Add to `backend/requirements.txt`:
```txt
fastapi-azure-auth==4.3.1
```

Redeploy backend after updating requirements.

### Step 5: Update Backend with Azure AD

Edit `backend/main.py`:

```python
import os
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from sqlmodel import Session, select
# ... other imports

# Azure AD Configuration
azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=os.getenv("APP_CLIENT_ID"),
    tenant_id=os.getenv("TENANT_ID"),
    scopes={
        f'api://{os.getenv("APP_CLIENT_ID")}/user_impersonation': 'user_impersonation',
    }
)

app = FastAPI(
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': os.getenv("OPENAPI_CLIENT_ID"),
    },
)

# Load OpenID config on startup
@app.on_event('startup')
async def load_config():
    await azure_scheme.openid_config.load_config()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "https://crm-frontend-dev.azurewebsites.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protected endpoint example
@app.get("/api/accounts", response_model=List[Account])
def get_accounts(
    session: Session = Depends(get_session),
    user=Security(azure_scheme, scopes=['user_impersonation'])
):
    if USE_SAMPLE_DATA:
        return get_sample_accounts()
    accounts = session.exec(select(Account)).all()
    return accounts

# ... rest of your endpoints
```

### Step 6: Configure Azure AD Environment Variables

```bash
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --settings \
    APP_CLIENT_ID="<your-app-client-id>" \
    TENANT_ID="<your-tenant-id>" \
    OPENAPI_CLIENT_ID="<your-openapi-client-id>"
```

### Step 7: Test Authentication

1. Go to: `https://crm-backend-dev.azurewebsites.net/docs`
2. Click **Authorize** button
3. Sign in with your Azure AD account
4. Test API endpoints

---

## Environment Configuration

### Backend Environment Variables Summary

```bash
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --settings \
    DATABASE_URL="postgresql://user:pass@server.postgres.database.azure.com:5432/crm_db?sslmode=require" \
    USE_SAMPLE_DATA="false" \
    APP_CLIENT_ID="your-app-client-id" \
    TENANT_ID="your-tenant-id" \
    OPENAPI_CLIENT_ID="your-openapi-client-id" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"
```

### View All Settings

```bash
az webapp config appsettings list \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --output table
```

---

## CI/CD with GitHub Actions

### Step 1: Get Publish Profile

```bash
# Download publish profile
az webapp deployment list-publishing-profiles \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --xml > backend-publish-profile.xml

# View content (you'll copy this to GitHub)
cat backend-publish-profile.xml
```

### Step 2: Add GitHub Secrets

In your GitHub repository:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets:
   - `AZURE_WEBAPP_PUBLISH_PROFILE_BACKEND`: Paste content from backend-publish-profile.xml
   - `AZURE_WEBAPP_PUBLISH_PROFILE_FRONTEND`: Same for frontend
   - `DATABASE_URL`: Your PostgreSQL connection string

### Step 3: Create GitHub Actions Workflow

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'crm-backend-dev'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE_BACKEND }}
          package: ./backend

  build-and-deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install and build
        run: |
          cd frontend
          npm install
          npm run build
      
      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'crm-frontend-dev'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE_FRONTEND }}
          package: ./frontend/dist
```

### Step 4: Push and Auto-Deploy

```bash
git add .github/workflows/azure-deploy.yml
git commit -m "Add Azure CI/CD workflow"
git push origin main
```

Now every push to `main` branch will auto-deploy to Azure!

---

## Monitoring & Troubleshooting

### View Live Logs

```bash
# Backend logs
az webapp log tail \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME

# Frontend logs
az webapp log tail \
  --resource-group $RESOURCE_GROUP \
  --name $FRONTEND_APP_NAME
```

### Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app crm-insights \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app crm-insights \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Configure backend to use it
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY="$INSTRUMENTATION_KEY"
```

### Common Issues

**Issue: "Application Error" page**
```bash
# Check logs
az webapp log tail --resource-group $RESOURCE_GROUP --name $BACKEND_APP_NAME

# Verify startup command
az webapp config show \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --query linuxFxVersion
```

**Issue: Database connection fails**
```bash
# Test connection from Azure
az postgres flexible-server execute \
  -n $PG_SERVER_NAME \
  -u $ADMIN_USER \
  -p "$ADMIN_PASSWORD" \
  -d crm_db \
  --querytext "SELECT 1;"

# Check firewall rules
az postgres flexible-server firewall-rule list \
  --resource-group $RESOURCE_GROUP \
  --name $PG_SERVER_NAME
```

**Issue: CORS errors**
- Update `allow_origins` in backend `main.py`
- Redeploy backend

### SSH into App Service

```bash
# Enable SSH
az webapp ssh --resource-group $RESOURCE_GROUP --name $BACKEND_APP_NAME
```

---

## Cost Estimation (Dev Environment)

| Resource | Tier | Monthly Cost (USD) |
|----------|------|-------------------|
| **App Service Plan (B1)** | Basic | ~$13 |
| **PostgreSQL Flexible (Burstable B1ms)** | 1 vCore, 32GB | ~$12 |
| **Total** | | **~$25/month** |

**Free Tier Option:**
- Use Free App Service tier (F1) - $0 but limited
- Use Basic PostgreSQL - still ~$12/month minimum

---

## Quick Reference Commands

```bash
# Resource Group
RESOURCE_GROUP="crm-dev-rg"
LOCATION="eastus"

# URLs
BACKEND_URL="https://crm-backend-dev.azurewebsites.net"
FRONTEND_URL="https://crm-frontend-dev.azurewebsites.net"

# Restart services
az webapp restart --resource-group $RESOURCE_GROUP --name crm-backend-dev
az webapp restart --resource-group $RESOURCE_GROUP --name crm-frontend-dev

# View all resources
az resource list --resource-group $RESOURCE_GROUP --output table

# Delete everything (cleanup)
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

---

## Next Steps

1. ✅ Deploy to Azure dev environment using this guide
2. ✅ Test all functionality
3. ✅ Set up Azure AD authentication
4. ✅ Configure CI/CD pipeline
5. 🔄 Create production environment (separate resource group)
6. 🔄 Set up custom domain
7. 🔄 Enable SSL/TLS
8. 🔄 Configure backup and disaster recovery

---

## Additional Resources

- **Azure App Service Docs**: https://learn.microsoft.com/azure/app-service/
- **Azure PostgreSQL Docs**: https://learn.microsoft.com/azure/postgresql/
- **FastAPI Azure Auth**: https://intility.github.io/fastapi-azure-auth/
- **Azure CLI Reference**: https://learn.microsoft.com/cli/azure/
- **Pricing Calculator**: https://azure.microsoft.com/pricing/calculator/

---

## Support

For issues specific to:
- **Azure**: Open ticket in Azure Portal
- **Application**: Check application logs and GitHub Issues
- **Authentication**: Review Azure AD App Registration settings

**Happy deploying!** 🚀
