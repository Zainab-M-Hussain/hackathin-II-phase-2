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
