from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

# Construct the path to the .env file, assuming it's in the 'backend' directory
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for debugging if .env is not loaded
if not DATABASE_URL:
    print("WARNING: DATABASE_URL not found in .env file or environment variables. Using a fallback SQLite database.")
    DATABASE_URL = "sqlite:///../../test.db"
else:
    print(f"DATABASE_URL loaded successfully: {DATABASE_URL}")


engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
