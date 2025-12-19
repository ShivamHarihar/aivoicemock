# CI/CD Pipeline Setup Guide

## Overview

This guide sets up a complete CI/CD pipeline using **GitHub Actions** for automated testing and deployment to Azure.

---

## Pipeline Stages

### 1. **Code Quality** ✅
- Black (code formatting)
- Flake8 (linting)
- Runs on every push/PR

### 2. **Unit Tests** ✅
- pytest with coverage
- Runs after code quality passes
- Uploads coverage reports

### 3. **Integration Tests** ✅
- Tests with Redis
- Tests free AI providers
- Validates end-to-end functionality

### 4. **Security Scan** ✅
- Safety (dependency vulnerabilities)
- Bandit (security issues)
- Generates security reports

### 5. **Build** ✅
- Creates deployment package
- Uploads artifacts

### 6. **Deploy to Staging** ✅
- Auto-deploys `develop` branch
- Runs smoke tests
- Environment: staging

### 7. **Deploy to Production** ✅
- Auto-deploys `main` branch
- Runs smoke tests + load tests
- Environment: production

### 8. **Post-Deployment** ✅
- Health checks
- Monitoring validation
- Notifications

---

## Setup Instructions

### Step 1: Create GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

#### Azure Credentials
```bash
# Get Azure credentials
az ad sp create-for-rbac \
  --name "github-actions-sampro" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/interview-system-rg \
  --sdk-auth

# Copy the JSON output and add as secret: AZURE_CREDENTIALS
```

#### API Keys
```
HF_API_KEY_1 = hf_your_key_here
HF_API_KEY_2 = hf_your_key_here
GROQ_API_KEY_1 = gsk_your_key_here
GROQ_API_KEY_2 = gsk_your_key_here
```

### Step 2: Create Azure Resources

```bash
# Staging environment
az webapp create \
  --name sampro-interview-staging \
  --resource-group interview-system-rg \
  --plan interview-plan \
  --runtime "PYTHON:3.8"

# Production environment (already created)
# sampro-interview-system
```

### Step 3: Configure Azure App Settings

```bash
# Set environment variables in Azure
az webapp config appsettings set \
  --name sampro-interview-system \
  --resource-group interview-system-rg \
  --settings \
    HF_API_KEY_1="$HF_API_KEY_1" \
    HF_API_KEY_2="$HF_API_KEY_2" \
    GROQ_API_KEY_1="$GROQ_API_KEY_1" \
    GROQ_API_KEY_2="$GROQ_API_KEY_2" \
    USE_FREE_AI="true" \
    REDIS_URL="redis://..." \
    AZURE_STORAGE_CONNECTION_STRING="..."
```

### Step 4: Enable GitHub Actions

1. Commit the workflow file:
```bash
git add .github/workflows/azure-deploy.yml
git commit -m "Add CI/CD pipeline"
git push origin main
```

2. Go to GitHub → Actions tab
3. You should see the workflow running!

---

## Branch Strategy

### Main Branch (`main`)
- **Protected branch**
- Requires PR approval
- Auto-deploys to **Production**
- Runs full test suite + load tests

### Develop Branch (`develop`)
- Development branch
- Auto-deploys to **Staging**
- Runs full test suite

### Feature Branches (`feature/*`)
- Create from `develop`
- Runs tests only (no deployment)
- Merge to `develop` via PR

---

## Workflow Triggers

### Automatic Triggers
```yaml
on:
  push:
    branches: [ main, develop ]  # Deploy on push
  pull_request:
    branches: [ main ]           # Test on PR
```

### Manual Trigger
```yaml
  workflow_dispatch:  # Manual trigger from GitHub UI
```

---

## Pipeline Flow Diagram

```
┌─────────────────┐
│  Push to Repo   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Code Quality   │ ← Black, Flake8
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Unit Tests     │ ← pytest + coverage
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Integration     │ ← Redis, AI providers
│ Tests           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Security Scan   │ ← Safety, Bandit
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Build Package  │
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ Deploy Staging │  │ Deploy Prod    │  │  Skip Deploy   │
│ (develop)      │  │ (main)         │  │ (feature/*)    │
└────────┬───────┘  └────────┬───────┘  └────────────────┘
         │                   │
         ▼                   ▼
┌────────────────┐  ┌────────────────┐
│  Smoke Tests   │  │ Smoke + Load   │
└────────┬───────┘  └────────┬───────┘
         │                   │
         └─────────┬─────────┘
                   ▼
         ┌─────────────────┐
         │ Post-Deployment │
         │  Health Checks  │
         └─────────────────┘
```

---

## Monitoring Pipeline

### View Pipeline Status

**GitHub Actions Tab:**
- See all workflow runs
- View logs for each job
- Download artifacts

**Azure Portal:**
- Monitor deployment slots
- View Application Insights
- Check resource health

### Pipeline Notifications

Add to workflow for Slack/Teams notifications:

```yaml
- name: Notify on Failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "❌ Deployment failed for ${{ github.ref }}"
      }
```

---

## Testing the Pipeline

### Test Code Quality
```bash
# Locally run what CI runs
black --check backend/
flake8 backend/
```

### Test Unit Tests
```bash
pytest backend/tests/ -v --cov=backend/src
```

### Test Integration
```bash
# Start Redis locally
docker run -d -p 6379:6379 redis:7-alpine

# Run tests
python test_huggingface_only.py
```

### Test Deployment Package
```bash
# Create package like CI does
mkdir -p deploy
cp -r backend deploy/
cp -r frontend deploy/

# Verify structure
ls -la deploy/
```

---

## Rollback Strategy

### Automatic Rollback
```yaml
- name: Rollback on Failure
  if: failure()
  run: |
    az webapp deployment slot swap \
      --name sampro-interview-system \
      --resource-group interview-system-rg \
      --slot staging \
      --target-slot production
```

### Manual Rollback
```bash
# Via Azure CLI
az webapp deployment slot swap \
  --name sampro-interview-system \
  --resource-group interview-system-rg \
  --slot production \
  --target-slot staging

# Or via Azure Portal
# App Service → Deployment slots → Swap
```

---

## Performance Optimization

### Cache Dependencies
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
```

### Parallel Jobs
```yaml
jobs:
  code-quality:
    # Runs in parallel
  unit-tests:
    needs: code-quality  # Waits for code-quality
  security-scan:
    # Runs in parallel with unit-tests
```

### Conditional Execution
```yaml
deploy-production:
  if: github.ref == 'refs/heads/main'  # Only on main branch
```

---

## Cost Optimization

### GitHub Actions Minutes

**Free tier:** 2,000 minutes/month
**Typical pipeline:** ~10 minutes
**Deployments/month:** 200 deployments free

**If you exceed:**
- Use self-hosted runners (free)
- Optimize job execution time
- Cache dependencies

---

## Security Best Practices

### 1. **Never Commit Secrets**
```bash
# Use GitHub Secrets for:
- API keys
- Azure credentials
- Database passwords
```

### 2. **Use Environment Protection**
```yaml
environment:
  name: production
  # Requires manual approval
```

### 3. **Scan Dependencies**
```yaml
- name: Dependency Check
  run: safety check
```

### 4. **Code Scanning**
```yaml
- name: Security Scan
  run: bandit -r backend/
```

---

## Troubleshooting

### Pipeline Fails on Tests
```bash
# Run tests locally first
pytest backend/tests/ -v

# Check test dependencies
pip install -r backend/requirements.txt
```

### Deployment Fails
```bash
# Check Azure credentials
az account show

# Verify app exists
az webapp show --name sampro-interview-system --resource-group interview-system-rg

# Check deployment logs
az webapp log tail --name sampro-interview-system --resource-group interview-system-rg
```

### Secrets Not Working
```bash
# Verify secrets are set
# GitHub → Settings → Secrets → Actions

# Test locally with env vars
export HF_API_KEY_1="hf_..."
python test_huggingface_only.py
```

---

## Next Steps

1. ✅ **Set up GitHub Secrets** (5 min)
2. ✅ **Create Azure staging environment** (10 min)
3. ✅ **Commit workflow file** (1 min)
4. ✅ **Push to trigger pipeline** (1 min)
5. ✅ **Monitor first deployment** (10 min)

**Total setup time: ~30 minutes**

---

## Summary

✅ **Automated CI/CD pipeline ready!**

**Features:**
- Automated testing on every commit
- Security scanning
- Staging + Production environments
- Automatic deployments
- Health checks
- Rollback capability

**Benefits:**
- Faster deployments (10 min vs 2 hours manual)
- Fewer errors (automated testing)
- Better security (automated scans)
- Easy rollbacks
- Audit trail

**Cost:** $0 (GitHub Actions free tier)
