"""
Configuration settings for the AI Model Router
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for the model router"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Model configurations
    DEFAULT_MODELS = {
        "gpt-3.5-turbo": {
            "max_tokens": 4096,
            "cost_per_1k_tokens": 0.5,
            "response_time_ms": 2000,
            "capabilities": ["text", "code", "analysis", "creative", "technical", "translation", "summarization", "qa"]
        },
        "gpt-4": {
            "max_tokens": 8192,
            "cost_per_1k_tokens": 30.0,
            "response_time_ms": 5000,
            "capabilities": ["text", "code", "analysis", "creative", "technical", "translation", "summarization", "qa"]
        },
        "gpt-4-turbo": {
            "max_tokens": 128000,
            "cost_per_1k_tokens": 10.0,
            "response_time_ms": 3000,
            "capabilities": ["text", "code", "analysis", "creative", "technical", "translation", "summarization", "qa"]
        }
    }
    
    # Routing thresholds
    COMPLEXITY_THRESHOLDS = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "expert": 4
    }
    
    # Cost optimization settings
    COST_OPTIMIZATION = {
        "max_cost_per_request": 1.0,  # USD
        "prefer_cheaper_models": True,
        "fallback_to_premium": True
    }
    
    # Performance settings
    PERFORMANCE = {
        "max_response_time_ms": 10000,
        "prefer_fast_models": False,
        "timeout_seconds": 30
    }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present"""
        if not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not found in environment variables")
            return False
        return True
