# Where to Add GitHub Secrets - Step-by-Step Guide

## 📍 Location: GitHub Repository Settings

You need to add these secrets in your **GitHub repository**, not in your local code.

---

## 🔐 Secrets to Add

```
AZURE_CREDENTIALS       (Azure service principal JSON)
HF_API_KEY_1           (Your first HuggingFace API key)
HF_API_KEY_2           (Your second HuggingFace API key - optional)
GROQ_API_KEY_1         (Your first Groq API key)
GROQ_API_KEY_2         (Your second Groq API key - optional)
```

---

## 📋 Step-by-Step Instructions

### Step 1: Go to Your GitHub Repository

1. Open your browser
2. Go to: `https://github.com/YOUR_USERNAME/sampro-ai-interview`
3. Make sure you're logged in to GitHub

---

### Step 2: Navigate to Settings

1. Click on **"Settings"** tab (top right of repository page)
   ```
   Code | Issues | Pull requests | Actions | Projects | Wiki | Security | Insights | Settings
                                                                                        ^^^^^^^^
   ```

2. You should see a sidebar on the left

---

### Step 3: Go to Secrets and Variables

1. In the left sidebar, find **"Secrets and variables"**
2. Click to expand it
3. Click on **"Actions"**

   ```
   Sidebar:
   ├── General
   ├── Access
   ├── Code and automation
   │   ├── Branches
   │   ├── Tags
   │   ├── Actions
   │   │   ├── General
   │   │   └── Runners
   │   ├── Webhooks
   │   └── Environments
   ├── Security
   │   ├── Code security and analysis
   │   └── Secrets and variables  ← Click here
   │       └── Actions            ← Then click here
   ```

---

### Step 4: Add New Secret

You'll see a page titled **"Actions secrets and variables"**

1. Click the green **"New repository secret"** button (top right)

---

### Step 5: Add AZURE_CREDENTIALS

#### First, Get Azure Credentials

Open PowerShell/Terminal and run:

```bash
az login

az ad sp create-for-rbac \
  --name "github-actions-sampro" \
  --role contributor \
  --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/interview-system-rg \
  --sdk-auth
```

**Replace `YOUR_SUBSCRIPTION_ID`** with your Azure subscription ID.

This will output JSON like:
```json
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",
  "tenantId": "xxx",
  ...
}
```

#### Add to GitHub:

1. **Name:** `AZURE_CREDENTIALS`
2. **Secret:** Paste the entire JSON output (all of it!)
3. Click **"Add secret"**

---

### Step 6: Add HF_API_KEY_1

1. Click **"New repository secret"** again
2. **Name:** `HF_API_KEY_1`
3. **Secret:** `hf_your_actual_key_here` (from your .env file)
4. Click **"Add secret"**

---

### Step 7: Add HF_API_KEY_2 (Optional)

1. Click **"New repository secret"** again
2. **Name:** `HF_API_KEY_2`
3. **Secret:** `hf_your_second_key_here`
4. Click **"Add secret"**

---

### Step 8: Add GROQ_API_KEY_1

1. Click **"New repository secret"** again
2. **Name:** `GROQ_API_KEY_1`
3. **Secret:** `gsk_your_actual_key_here` (from your .env file)
4. Click **"Add secret"**

---

### Step 9: Add GROQ_API_KEY_2 (Optional)

1. Click **"New repository secret"** again
2. **Name:** `GROQ_API_KEY_2`
3. **Secret:** `gsk_your_second_key_here`
4. Click **"Add secret"**

---

## ✅ Verification

After adding all secrets, you should see them listed:

```
Repository secrets:
├── AZURE_CREDENTIALS         Updated X minutes ago
├── HF_API_KEY_1             Updated X minutes ago
├── HF_API_KEY_2             Updated X minutes ago
├── GROQ_API_KEY_1           Updated X minutes ago
└── GROQ_API_KEY_2           Updated X minutes ago
```

**Note:** You won't be able to view the secret values after adding them (for security).

---

## 🎯 Quick Reference

### Where to Find Your Keys

**HuggingFace Keys:**
- Open your `.env` file
- Look for: `HF_API_KEY_1=hf_...`
- Copy everything after the `=`

**Groq Keys:**
- Open your `.env` file
- Look for: `GROQ_API_KEY_1=gsk_...`
- Copy everything after the `=`

**Azure Credentials:**
- Run the `az ad sp create-for-rbac` command
- Copy the entire JSON output

---

## 🔍 Visual Path

```
GitHub.com
  └── Your Repository (sampro-ai-interview)
      └── Settings (top tab)
          └── Secrets and variables (left sidebar)
              └── Actions
                  └── New repository secret (green button)
                      ├── Name: AZURE_CREDENTIALS
                      ├── Secret: {paste JSON}
                      └── Add secret (button)
```

---

## 🐛 Troubleshooting

### "I don't see Settings tab"
- You need to be the repository owner or have admin access
- If it's a fork, you need to add secrets to your fork

### "Azure CLI command fails"
- Make sure you're logged in: `az login`
- Get your subscription ID: `az account show --query id -o tsv`
- Replace `YOUR_SUBSCRIPTION_ID` in the command

### "I don't have a resource group yet"
- That's okay! The resource group will be created during deployment
- You can use any subscription ID for now
- Or create resource group first: `az group create --name interview-system-rg --location eastus`

---

## 📝 Example

Here's what it looks like when adding a secret:

```
┌─────────────────────────────────────────────┐
│ New secret                                  │
├─────────────────────────────────────────────┤
│                                             │
│ Name *                                      │
│ ┌─────────────────────────────────────────┐ │
│ │ HF_API_KEY_1                            │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Secret *                                    │
│ ┌─────────────────────────────────────────┐ │
│ │ hf_AbCdEfGhIjKlMnOpQrStUvWxYz12345     │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ [Cancel]              [Add secret]          │
└─────────────────────────────────────────────┘
```

---

## ⚠️ Important Notes

1. **Never commit secrets to code** - Always use GitHub Secrets
2. **Secrets are encrypted** - GitHub encrypts them at rest
3. **Can't view after adding** - You can only update or delete
4. **Case sensitive** - Use exact names: `HF_API_KEY_1` not `hf_api_key_1`
5. **No spaces** - Secret names can't have spaces

---

## ✅ After Adding Secrets

Once all secrets are added:

1. **Commit your code:**
   ```bash
   git add .
   git commit -m "Add CI/CD pipeline"
   git push origin main
   ```

2. **Watch the pipeline:**
   - Go to **Actions** tab in GitHub
   - See your workflow running
   - Check for green checkmarks ✅

3. **Verify deployment:**
   - After pipeline completes
   - Visit: `https://sampro-interview-system.azurewebsites.net/health`
   - Should see: `{"status": "healthy", ...}`

---

## 🎉 You're Done!

Your secrets are now configured and the CI/CD pipeline will use them automatically!

**Next time you push code:**
1. Tests run automatically ✅
2. Code deploys to Azure ✅
3. Health checks verify deployment ✅
4. You get notified of results ✅

**All automated!** 🚀
