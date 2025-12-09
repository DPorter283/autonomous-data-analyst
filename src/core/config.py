import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# 1. Load .env variables into the actual OS environment
# This ensures 'boto3' and 'ChatBedrock' can find your AWS keys automatically.
load_dotenv()

class Settings(BaseSettings):
    """
    Application Settings & Environment Variables.
    """
    # We map 'aws_region' to the env var 'AWS_DEFAULT_REGION'
    aws_region: str = Field(default="us-east-1", alias="AWS_DEFAULT_REGION")
    
    # Model IDs
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0" 

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # 2. CRITICAL: Tell Pydantic to ignore other keys in .env (like AWS_ACCESS_KEY_ID)
        # instead of throwing a ValidationError.
        extra = "ignore"

# Instantiate global settings
settings = Settings()
