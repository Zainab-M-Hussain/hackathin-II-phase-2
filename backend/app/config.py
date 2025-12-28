import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "super-secret-key") # TODO: Replace with a strong, randomly generated secret in production
if SECRET_KEY == "super-secret-key":
    # In a real production environment, you might want to raise an exception here
    # to prevent the app from starting with a default, insecure key.
    pass

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# MCP Server Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8080")  # Default MCP server URL
MCP_TIMEOUT = int(os.getenv("MCP_TIMEOUT", "30"))  # Timeout for MCP requests in seconds
MCP_MAX_RETRIES = int(os.getenv("MCP_MAX_RETRIES", "3"))  # Number of retries for failed requests
