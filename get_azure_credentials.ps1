# Get Azure Credentials for GitHub Secrets (PowerShell)
# Run this in PowerShell on Windows

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Get Azure Credentials for GitHub" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
$azInstalled = Get-Command az -ErrorAction SilentlyContinue

if (-not $azInstalled) {
    Write-Host "❌ Azure CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Azure CLI first:"
    Write-Host "  Download from: https://aka.ms/installazurecliwindows"
    exit 1
}

Write-Host "✓ Azure CLI found" -ForegroundColor Green
Write-Host ""

# Login to Azure
Write-Host "Step 1: Logging in to Azure..." -ForegroundColor Yellow
az login

# Get subscription ID
Write-Host ""
Write-Host "Step 2: Getting your subscription ID..." -ForegroundColor Yellow
$subscriptionId = az account show --query id -o tsv

if (-not $subscriptionId) {
    Write-Host "❌ Could not get subscription ID" -ForegroundColor Red
    Write-Host "Please make sure you're logged in: az login"
    exit 1
}

Write-Host "✓ Subscription ID: $subscriptionId" -ForegroundColor Green
Write-Host ""

# Create service principal
Write-Host "Step 3: Creating service principal..." -ForegroundColor Yellow
Write-Host "(This will be used by GitHub Actions to deploy to Azure)"
Write-Host ""

$timestamp = [int][double]::Parse((Get-Date -UFormat %s))
$credentials = az ad sp create-for-rbac `
  --name "github-actions-sampro-$timestamp" `
  --role contributor `
  --scopes /subscriptions/$subscriptionId `
  --sdk-auth

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Copy the JSON below and add it as AZURE_CREDENTIALS in GitHub:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "────────────────────────────────────" -ForegroundColor Cyan
    Write-Host $credentials
    Write-Host "────────────────────────────────────" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Copy the JSON above (everything between the lines)"
    Write-Host "2. Go to GitHub → Your Repo → Settings → Secrets and variables → Actions"
    Write-Host "3. Click 'New repository secret'"
    Write-Host "4. Name: AZURE_CREDENTIALS"
    Write-Host "5. Secret: Paste the JSON"
    Write-Host "6. Click 'Add secret'"
    Write-Host ""
    
    # Also save to file
    $credentials | Out-File -FilePath "azure_credentials.json" -Encoding UTF8
    Write-Host "✓ Credentials also saved to: azure_credentials.json" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "❌ Failed to create service principal" -ForegroundColor Red
    Write-Host "Please check your Azure permissions"
    exit 1
}
