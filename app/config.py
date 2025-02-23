import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

class Config:
    # ✅ Use Cloud SQL Instance Connection Name
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://subdomain:ex4KjgDLFgygyat1EcV3@/newsletter?host=/cloudsql/subdomain-systems-llc:us-central1:sds-prod-shopify"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    API_KEY = os.getenv("API_KEY")  # 🔒 Load API Key from environment variables
