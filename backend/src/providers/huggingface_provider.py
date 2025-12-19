"""
HuggingFace Provider - Free AI provider with multi-account rotation
Supports Mixtral, Llama 3, and other open-source models
"""

import os
import asyncio
import logging
from typing import Optional, List
from huggingface_hub import InferenceClient
from backend.src.ai_provider_manager import BaseAIProvider

logger = logging.getLogger(__name__)


class HuggingFaceProvider(BaseAIProvider):
    """
    HuggingFace Inference API provider with multi-account rotation.
    Free tier: ~1000 requests/hour per account (rate-limited, not hard capped)
    """
    
    def __init__(self, num_accounts: int = 20):
        """
        Initialize HuggingFace provider with multiple accounts
        
        Args:
            num_accounts: Number of HF accounts to rotate through
        """
        super().__init__("huggingface")
        
        # Load API keys from environment
        self.api_keys = self._load_api_keys(num_accounts)
        
        if not self.api_keys:
            logger.warning("No HuggingFace API keys found!")
            self.clients = []
        else:
            # Create clients for each API key
            self.clients = [
                InferenceClient(token=key) 
                for key in self.api_keys
            ]
            logger.info(f"Initialized {len(self.clients)} HuggingFace clients")
        
        self.current_index = 0
        
        # Recommended models (in priority order) - Updated for 2025
        self.models = [
            "meta-llama/Meta-Llama-3.1-8B-Instruct",      # Latest Llama 3.1
            "mistralai/Mistral-7B-Instruct-v0.3",         # Latest Mistral
            "microsoft/Phi-3-mini-4k-instruct",           # Fast and efficient
            "google/gemma-7b-it"                          # Google's Gemma
        ]
        self.current_model = self.models[0]
        
        # No hard daily limit for HF, just rate limiting
        self.daily_limit = None
    
    def _load_api_keys(self, num_accounts: int) -> List[str]:
        """Load API keys from environment variables"""
        keys = []
        
        for i in range(1, num_accounts + 1):
            key = os.getenv(f'HF_API_KEY_{i}')
            if key:
                keys.append(key)
        
        # Fallback to single key
        if not keys:
            single_key = os.getenv('HF_API_KEY') or os.getenv('HUGGINGFACE_API_KEY')
            if single_key:
                keys.append(single_key)
        
        logger.info(f"Loaded {len(keys)} HuggingFace API keys")
        return keys
    
    def get_next_client(self) -> InferenceClient:
        """Get next client in round-robin fashion"""
        if not self.clients:
            raise Exception("No HuggingFace clients available")
        
        client = self.clients[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.clients)
        return client
    
    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> str:
        """
        Generate AI response using HuggingFace Inference API
        
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
                client = self.get_next_client()
                
                # Python 3.8 compatible async wrapper
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: client.chat_completion(
                        messages=messages,
                        model=self.current_model,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                )
                
                # Extract response text
                if response and response.choices:
                    text = response.choices[0].message.content
                    self.request_count += 1
                    return text.strip()
                else:
                    raise Exception("Empty response from HuggingFace")
                
            except Exception as e:
                last_error = e
                logger.warning(f"HuggingFace attempt {attempt + 1} failed: {str(e)}")
                
                # If rate limited, try next account immediately
                if "rate" in str(e).lower() or "429" in str(e):
                    logger.info("Rate limited, trying next account...")
                    continue
                
                # For other errors, wait before retry
                if attempt < max_retries - 1:
                    await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
        
        # All retries failed
        raise Exception(f"HuggingFace failed after {max_retries} attempts: {last_error}")
    
    def has_quota(self) -> bool:
        """HuggingFace has no hard daily limit, just rate limiting"""
        return len(self.clients) > 0
    
    def switch_model(self, model_index: int = None):
        """
        Switch to a different model
        
        Args:
            model_index: Index in self.models list, or None for next model
        """
        if model_index is not None:
            if 0 <= model_index < len(self.models):
                self.current_model = self.models[model_index]
        else:
            # Cycle to next model
            current_idx = self.models.index(self.current_model)
            next_idx = (current_idx + 1) % len(self.models)
            self.current_model = self.models[next_idx]
        
        logger.info(f"Switched to model: {self.current_model}")
