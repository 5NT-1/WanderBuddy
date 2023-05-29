import os
import logging
import uuid
from dotenv import load_dotenv
from supabase.client import create_client, Client
from telegram import Update, File
from telegram.ext import ContextTypes

load_dotenv()

url: str = os.environ.get("SUPABASE_PROJECT_URL")
key: str = os.environ.get("SUPABASE_PROJECT_ANON_KEY")
supabase: Client = create_client(url, key)

source = "images/hero.jpg"
logger = logging.getLogger(__name__)

def convert_uuid_to_url(uuid: str):
    return f"{url}/storage/v1/object/public/photos/{uuid}"

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ensures that the user is in a route
    if "current_route_id" not in context.user_data or context.user_data["current_route_id"] < 0:
        await update.message.reply_text("Sorry! Please select a route before adding a picture!")
        return
    file: str = update.message.photo[-1].file_id
    obj: File = await context.bot.get_file(file)
    temp_file_name = "temp.jpg"
    unique_id = str(uuid.uuid4())
    await obj.download_to_drive(temp_file_name)
    res = supabase.storage.from_('photos').upload(unique_id, temp_file_name)
    # Gets the location_id of the current location in the route
    data, count = supabase.table('route_has_location').select("*").match({
        "route_id": context.user_data["current_route_id"], 
        "index": context.user_data["current_routes"][context.user_data["current_route_id"]]
        }).execute()
    # Updates photos table of 
    supabase.table('photos').insert({
        "location_id": data[1][0]["location_id"],
        "url": unique_id
    }).execute()

    os.remove(temp_file_name)
    
    await update.message.reply_text("Image received")

# with open(source, 'rb+') as f:
#   res = supabase.storage.from_('photos').upload("ab.jpg", os.path.abspath(source))
#   print(res.json())
