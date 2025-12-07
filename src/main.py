import boto3
from src.core.config import settings

def test_connection():
    print(f"📡 Connecting to AWS Bedrock ({settings.aws_region})...")

    client = boto3.client(
        "bedrock-runtime", 
        region_name=settings.aws_region
    )

    payload = '{"anthropic_version": "bedrock-2023-05-31", "max_tokens": 100, "messages": [{"role": "user", "content": "Hello! Are you online?"}]}'

    try:
        response = client.invoke_model(
            modelId=settings.model_id,
            body=payload
        )
        print("✅ Success! AWS Bedrock responded.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()
