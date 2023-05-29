import os
from dotenv import load_dotenv
from supabase.client import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_PROJECT_URL")
key: str = os.environ.get("SUPABASE_PROJECT_ANON_KEY")
supabase: Client = create_client(url, key)