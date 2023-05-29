import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_PROJECT_URL")
key: str = os.environ.get("SUPABASE_PROJECT_ANON_KEY")
supabase: Client = create_client(url, key)
response = supabase.table('trip').select("*").execute()
print(response)
# data=[{'id': 1, 'created_at': '2023-05-29T09:35:10.495316+00:00', 'name': 'test', 'user_id': 'test1'}] count=None

