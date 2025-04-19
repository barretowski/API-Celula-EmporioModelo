from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

print("SECRET_KEY:", SECRET_KEY)
print("DATABASE_URL:", DATABASE_URL)
