import os
from dotenv import load_dotenv
from supabase.client import create_client, Client
from telegram import Update, File
from telegram.ext import ContextTypes

load_dotenv()

url: str = os.environ.get("SUPABASE_PROJECT_URL")
key: str = os.environ.get("SUPABASE_PROJECT_ANON_KEY")
supabase: Client = create_client(url, key)

source = "images/hero.jpg"

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file: str = update.message.photo[-1].file_id
    obj: File = await context.bot.get_file(file)
    file_name = "name.jpg"
    await obj.download_to_drive(file_name)
    res = supabase.storage.from_('photos').upload("zzz.jpg", file_name)
    os.remove(file_name)
    
    await update.message.reply_text("Image received")

# with open(source, 'rb+') as f:
#   res = supabase.storage.from_('photos').upload("ab.jpg", os.path.abspath(source))
#   print(res.json())
