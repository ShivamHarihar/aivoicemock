# Free AI System - Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
cd d:\sampro-project-ai\sampro-ai-interview\backend
pip install -r requirements_free_ai.txt
```

### Step 2: Get Free API Keys

#### HuggingFace (Recommended - Start with 3-5 accounts)
1. Go to https://huggingface.co/join
2. Create account with email
3. Go to https://huggingface.co/settings/tokens
4. Click "New token" → Name it → Copy token
5. Repeat for multiple accounts (use different emails)

#### Groq (Recommended - Start with 2-3 accounts)
1. Go to https://console.groq.com/
2. Sign up with email
3. Go to API Keys section
4. Create new API key → Copy it
5. Repeat for multiple accounts

### Step 3: Configure Environment

```bash
# Copy template
cp .env.free_ai.template .env

# Edit .env and add your API keys
# Example:
HF_API_KEY_1=hf_abc123...
HF_API_KEY_2=hf_def456...
GROQ_API_KEY_1=gsk_xyz789...
GROQ_API_KEY_2=gsk_uvw012...
```

### Step 4: Test the System

```python
# Run this test script
python -c "
from backend.src.init_free_ai import initialize_free_ai_system, get_ai_response, print_system_status

# Initialize
ai_manager = initialize_free_ai_system()

# Test request
response = get_ai_response('Say hello!')
print(f'AI Response: {response}')

# Check status
print_system_status()
"
```

## 📊 Expected Capacity

With minimal setup (3 HF + 2 Groq accounts):
- **HuggingFace:** 3 accounts × ~20,000/day = **60,000 requests/day**
- **Groq:** 2 accounts × 14,400/day = **28,800 requests/day**
- **Total:** **88,800 requests/day**
- **With 80% cache:** Can handle **444,000 requests/day** (enough for 26,000+ interviews!)

## 🎯 Scaling to 10,000 Interviews/Day

For full capacity (10,000 interviews = ~170,000 requests):

1. **Create More Accounts:**
   - 10-20 HuggingFace accounts
   - 5-10 Groq accounts

2. **Enable Caching:**
   - Install Redis: `pip install redis`
   - Start Redis: `redis-server`
   - Set `CACHE_BACKEND=redis` in `.env`

3. **Monitor Usage:**
   ```python
   from backend.src.init_free_ai import print_system_status
   print_system_status()  # Run this periodically
   ```

## 🔧 Integration with Interview Engine

The system is designed to be a drop-in replacement for your current Groq client:

```python
# OLD CODE (using single Groq account):
from backend.src.grok_client import client
response = client.chat.completions.create(...)

# NEW CODE (using free AI system):
from backend.src.init_free_ai import get_ai_response_async
response = await get_ai_response_async(prompt, context)
```

## 📈 Monitoring

Check system status anytime:

```python
from backend.src.init_free_ai import print_system_status
print_system_status()
```

Output example:
```
============================================================
FREE AI SYSTEM STATUS
============================================================

📊 Overall Statistics:
  Total Requests: 1,234
  Cache Hit Rate: 78.5%
  Requests/Min: 45.2

💾 Cache Statistics:
  Backend: memory
  Hit Rate: 78.5%
  Hits: 969
  Misses: 265

🤖 Provider Status:
  ✓ Huggingface: 456 requests today
  ✓ Groq: 513 requests today

  Groq Details:
    Used: 513 / 28,800
    Remaining: 28,287
    Usage: 1.8%
============================================================
```

## ⚠️ Important Notes

1. **Account Creation:**
   - Use legitimate email addresses
   - Don't create too many accounts from same IP in short time
   - Spread account creation over a few days

2. **Usage Limits:**
   - HuggingFace: Rate-limited but no hard daily cap
   - Groq: 14,400 requests/day per account (hard limit)
   - System automatically rotates between accounts

3. **Caching:**
   - 80%+ cache hit rate expected after first day
   - Dramatically reduces actual API calls
   - Responses cached for 24 hours

## 🐛 Troubleshooting

**"No AI providers available"**
- Check your `.env` file has API keys
- Verify API keys are valid (test on provider website)
- Check logs for specific errors

**"Rate limited"**
- System will automatically try next account
- If all accounts rate-limited, wait a few minutes
- Consider adding more accounts

**"All providers exhausted"**
- Check daily quotas with `print_system_status()`
- Add more accounts or wait for daily reset
- Enable caching to reduce API calls

## 📞 Next Steps

1. ✅ Install dependencies
2. ✅ Get 2-3 API keys from each provider
3. ✅ Configure `.env` file
4. ✅ Test with sample request
5. 🔄 Integrate with interview engine (next phase)
6. 📊 Monitor and scale as needed

**You're now ready to handle thousands of interviews per day at ZERO cost!** 🎉
