import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application Settings & Environment Variables.
    Validation is automatic. If a variable is missing, the app crashes early (Good!).
    """
    # AWS Credentials (loaded from environment)
    aws_region: str = Field(default="us-east-1", env="AWS_DEFAULT_REGION")

    # Model IDs
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0" 

    class Config:
        env_file = ".env"

# Instantiate global settings
settings = Settings()
