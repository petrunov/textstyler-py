import os
from dotenv import load_dotenv

load_dotenv()  

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        raise Exception("OPENAI_API_KEY is not set. Please set it in your environment or .env file.")

settings = Settings()