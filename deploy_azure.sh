#!/bin/bash

# Quick Deploy Script for Azure
# Run this to deploy your app to Azure

set -e  # Exit on error

echo "======================================"
echo "Sampro Interview System - Azure Deploy"
echo "======================================"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if logged in
echo "Checking Azure login..."
az account show &> /dev/null || {
    echo "Not logged in to Azure. Logging in..."
    az login
}

# Configuration
RESOURCE_GROUP="interview-system-rg"
APP_NAME="sampro-interview-system"
LOCATION="eastus"
PLAN_NAME="interview-plan"
SKU="P1V3"

echo ""
echo "Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  App Name: $APP_NAME"
echo "  Location: $LOCATION"
echo "  SKU: $SKU"
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

# Create resource group if it doesn't exist
echo "Creating resource group..."
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output none || echo "Resource group already exists"

# Create App Service Plan if it doesn't exist
echo "Creating App Service Plan..."
az appservice plan create \
    --name $PLAN_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku $SKU \
    --is-linux \
    --output none || echo "App Service Plan already exists"

# Create Web App if it doesn't exist
echo "Creating Web App..."
az webapp create \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --plan $PLAN_NAME \
    --runtime "PYTHON:3.8" \
    --output none || echo "Web App already exists"

# Configure startup command
echo "Configuring startup command..."
az webapp config set \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --startup-file "startup.sh" \
    --output none

# Deploy code
echo "Deploying code..."
az webapp up \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --runtime "PYTHON:3.8" \
    --sku $SKU \
    --location $LOCATION

echo ""
echo "======================================"
echo "✅ Deployment Complete!"
echo "======================================"
echo ""
echo "Your app is available at:"
echo "  https://$APP_NAME.azurewebsites.net"
echo ""
echo "Next steps:"
echo "  1. Configure environment variables in Azure Portal"
echo "  2. Add your API keys (HF_API_KEY_1, GROQ_API_KEY_1, etc.)"
echo "  3. Test the health endpoint: https://$APP_NAME.azurewebsites.net/health"
echo ""
