"""
Groq Provider - Fast inference with free tier
Supports Llama 3 and Mixtral models with multi-account rotation
"""

import os
import asyncio
import logging
from typing import Optional, List
from datetime import datetime, timedelta
from groq import Groq
from backend.src.ai_provider_manager import BaseAIProvider

logger = logging.getLogger(__name__)


class GroqProvider(BaseAIProvider):
    """
    Groq AI provider with multi-account rotation.
    Free tier: 14,400 requests/day per account
    """
    
    def __init__(self, num_accounts: int = 10):
        """
        Initialize Groq provider with multiple accounts
        
        Args:
            num_accounts: Number of Groq accounts to rotate through
        """
        super().__init__("groq")
        
        # Load API keys
        self.api_keys = self._load_api_keys(num_accounts)
        
        if not self.api_keys:
            logger.warning("No Groq API keys found!")
            self.clients = []
        else:
            # Create clients for each API key
            self.clients = [
                Groq(api_key=key)
                for key in self.api_keys
            ]
            logger.info(f"Initialized {len(self.clients)} Groq clients")
        
        self.current_index = 0
        
        # Track usage per account
        self.account_usage = [0] * len(self.clients)
        self.last_reset = datetime.now()
        
        # Groq free tier limit
        self.daily_limit_per_account = 14400
        self.daily_limit = self.daily_limit_per_account * len(self.clients)
        
        # Recommended models
        self.models = [
            "llama3-70b-8192",      # Best quality, 8K context
            "mixtral-8x7b-32768",   # Good quality, 32K context
            "llama3-8b-8192"        # Fastest, 8K context
        ]
        self.current_model = self.models[0]
    
    def _load_api_keys(self, num_accounts: int) -> List[str]:
        """Load API keys from environment variables"""
        keys = []
        
        for i in range(1, num_accounts + 1):
            key = os.getenv(f'GROQ_API_KEY_{i}')
            if key:
                keys.append(key)
        
        # Fallback to single key
        if not keys:
            single_key = os.getenv('GROQ_API_KEY')
            if single_key:
                keys.append(single_key)
        
        logger.info(f"Loaded {len(keys)} Groq API keys")
        return keys
    
    def _check_daily_reset(self):
        """Reset usage counters if it's a new day"""
        now = datetime.now()
        if (now - self.last_reset) > timedelta(days=1):
            self.account_usage = [0] * len(self.clients)
            self.request_count = 0
            self.last_reset = now
            logger.info("Groq daily usage counters reset")
    
    def get_next_client(self):
        """Get next available client with quota"""
        self._check_daily_reset()
        
        if not self.clients:
            raise Exception("No Groq clients available")
        
        # Find account with lowest usage
        min_usage_idx = self.account_usage.index(min(self.account_usage))
        
        # Check if this account has quota
        if self.account_usage[min_usage_idx] >= self.daily_limit_per_account:
            raise Exception("All Groq accounts exhausted for today")
        
        return self.clients[min_usage_idx], min_usage_idx
    
    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> str:
        """
        Generate AI response using Groq API
        
        Args:
            prompt: User prompt
            context: System context
            max_tokens: Maximum response length
            temperature: Response randomness
            max_retries: Number of retry attempts
            
        Returns:
            Generated text response
        """
        
        # Build messages
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                client, account_idx = self.get_next_client()
                
                # Python 3.8 compatible async wrapper
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: client.chat.completions.create(
                        model=self.current_model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                )
                
                # Extract response text
                if response and response.choices:
                    text = response.choices[0].message.content
                    
                    # Update usage counters
                    self.account_usage[account_idx] += 1
                    self.request_count += 1
                    
                    return text.strip()
                else:
                    raise Exception("Empty response from Groq")
                
            except Exception as e:
                last_error = e
                logger.warning(f"Groq attempt {attempt + 1} failed: {str(e)}")
                
                # If rate limited, try next account
                if "rate" in str(e).lower() or "429" in str(e):
                    logger.info("Rate limited, trying next account...")
                    continue
                
                # For other errors, wait before retry
                if attempt < max_retries - 1:
                    await asyncio.sleep(0.5 * (attempt + 1))
        
        # All retries failed
        raise Exception(f"Groq failed after {max_retries} attempts: {last_error}")
    
    def has_quota(self) -> bool:
        """Check if any account has remaining quota"""
        self._check_daily_reset()
        
        if not self.clients:
            return False
        
        # Check if at least one account has quota
        return any(usage < self.daily_limit_per_account for usage in self.account_usage)
    
    def get_usage_stats(self):
        """Get detailed usage statistics"""
        self._check_daily_reset()
        
        total_used = sum(self.account_usage)
        total_available = self.daily_limit
        
        return {
            'total_used': total_used,
            'total_available': total_available,
            'remaining': total_available - total_used,
            'usage_percentage': round((total_used / total_available * 100), 2) if total_available > 0 else 0,
            'accounts': len(self.clients),
            'per_account_usage': self.account_usage
        }
    
    def switch_model(self, model_index: int = None):
        """Switch to a different model"""
        if model_index is not None:
            if 0 <= model_index < len(self.models):
                self.current_model = self.models[model_index]
        else:
            current_idx = self.models.index(self.current_model)
            next_idx = (current_idx + 1) % len(self.models)
            self.current_model = self.models[next_idx]
        
        logger.info(f"Switched to model: {self.current_model}")
