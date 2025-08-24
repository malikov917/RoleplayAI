import os
from typing import Optional
from dotenv import load_dotenv

class Settings:

    load_dotenv()

# Real OpenAI integration with production settings
    # Supabase Configuration
    SUPABASE_URL: str = "https://hztouzzhafevtrnysvrn.supabase.co"
    SUPABASE_ANON_KEY: str = os.getenv('SUPABASE_ANON_KEY')
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres.hztouzzhafevtrnysvrn:[YOUR_PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
    
    # OpenAI Configuration
    
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL: str = "gpt-4o-mini"  # Using GPT-4o-mini for better performance and cost efficiency
    OPENAI_MAX_TOKENS: int = 150
    OPENAI_TEMPERATURE: float = 0.8
    
    # App Configuration
    APP_NAME: str = "AI Roleplay Trainer"
    DEBUG: bool = True
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES: int = 60
    MAX_MESSAGES_PER_SESSION: int = 100

settings = Settings()