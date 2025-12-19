# Quick Guide: Adding GitHub Secrets

## 🎯 Where to Add Secrets

**Location:** GitHub.com → Your Repository → Settings → Secrets and variables → Actions

**URL Format:** `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`

---

## 📝 Secrets to Add

| Secret Name | Value | Where to Get It |
|-------------|-------|-----------------|
| `AZURE_CREDENTIALS` | JSON from Azure CLI | Run `get_azure_credentials.ps1` |
| `HF_API_KEY_1` | `hf_...` | From your `.env` file |
| `HF_API_KEY_2` | `hf_...` | From your `.env` file (optional) |
| `GROQ_API_KEY_1` | `gsk_...` | From your `.env` file |
| `GROQ_API_KEY_2` | `gsk_...` | From your `.env` file (optional) |

---

## ⚡ Quick Steps

### 1. Get Azure Credentials (Windows)

```powershell
# Run in PowerShell
.\get_azure_credentials.ps1
```

This will:
- Login to Azure
- Create service principal
- Display JSON to copy
- Save to `azure_credentials.json`

### 2. Get Your API Keys

Open your `.env` file and copy the values:

```bash
# From .env file:
HF_API_KEY_1=hf_abc123...     ← Copy this value
HF_API_KEY_2=hf_def456...     ← Copy this value
GROQ_API_KEY_1=gsk_xyz789...  ← Copy this value
GROQ_API_KEY_2=gsk_uvw012...  ← Copy this value
```

### 3. Add to GitHub

1. **Go to:** `https://github.com/YOUR_USERNAME/sampro-ai-interview/settings/secrets/actions`

2. **Click:** "New repository secret" (green button)

3. **Add each secret:**
   - Name: `AZURE_CREDENTIALS`
   - Secret: Paste JSON from step 1
   - Click "Add secret"
   
   - Name: `HF_API_KEY_1`
   - Secret: Paste value from .env
   - Click "Add secret"
   
   - Name: `GROQ_API_KEY_1`
   - Secret: Paste value from .env
   - Click "Add secret"

---

## ✅ Verify

After adding, you should see:

```
Repository secrets:
├── AZURE_CREDENTIALS
├── HF_API_KEY_1
├── HF_API_KEY_2
├── GROQ_API_KEY_1
└── GROQ_API_KEY_2
```

---

## 🚀 Test It

```bash
# Commit and push
git add .
git commit -m "Add CI/CD pipeline"
git push origin main

# Watch pipeline run
# Go to: https://github.com/YOUR_USERNAME/sampro-ai-interview/actions
```

---

## 📞 Need Help?

See detailed guide: `GITHUB_SECRETS_GUIDE.md`
