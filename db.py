import os
from dotenv import load_dotenv
from supabase.client import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_PROJECT_URL")
key: str = os.environ.get("SUPABASE_PROJECT_ANON_KEY")
supabase: Client = create_client(url, key)

source = "images/hero.jpg"

with open(source, 'rb+') as f:
  res = supabase.storage.from_('photos').upload("ab.jpg", os.path.abspath(source))
  print(res.json())
