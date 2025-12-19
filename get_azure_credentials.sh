#!/bin/bash

# Get Azure Credentials for GitHub Secrets
# This script helps you get the AZURE_CREDENTIALS value

echo "======================================"
echo "Get Azure Credentials for GitHub"
echo "======================================"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found!"
    echo ""
    echo "Please install Azure CLI first:"
    echo "  Windows: https://aka.ms/installazurecliwindows"
    echo "  Mac: brew install azure-cli"
    echo "  Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
    exit 1
fi

echo "✓ Azure CLI found"
echo ""

# Login to Azure
echo "Step 1: Logging in to Azure..."
az login

# Get subscription ID
echo ""
echo "Step 2: Getting your subscription ID..."
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

if [ -z "$SUBSCRIPTION_ID" ]; then
    echo "❌ Could not get subscription ID"
    echo "Please make sure you're logged in: az login"
    exit 1
fi

echo "✓ Subscription ID: $SUBSCRIPTION_ID"
echo ""

# Create service principal
echo "Step 3: Creating service principal..."
echo "(This will be used by GitHub Actions to deploy to Azure)"
echo ""

CREDENTIALS=$(az ad sp create-for-rbac \
  --name "github-actions-sampro-$(date +%s)" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID \
  --sdk-auth)

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ SUCCESS!"
    echo "======================================"
    echo ""
    echo "Copy the JSON below and add it as AZURE_CREDENTIALS in GitHub:"
    echo ""
    echo "────────────────────────────────────"
    echo "$CREDENTIALS"
    echo "────────────────────────────────────"
    echo ""
    echo "Next steps:"
    echo "1. Copy the JSON above (everything between the lines)"
    echo "2. Go to GitHub → Your Repo → Settings → Secrets and variables → Actions"
    echo "3. Click 'New repository secret'"
    echo "4. Name: AZURE_CREDENTIALS"
    echo "5. Secret: Paste the JSON"
    echo "6. Click 'Add secret'"
    echo ""
else
    echo "❌ Failed to create service principal"
    echo "Please check your Azure permissions"
    exit 1
fi
