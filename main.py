import os
import logging
from dotenv import load_dotenv
from telegram import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          ConversationHandler, InlineQueryHandler,
                          MessageHandler, filters)
from store import create_tables, db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

NEW_TRIP, LOCATION_COUNT, ATTRACTION = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user if they want to start new trip."""
    reply_keyboard =[["Yes", "No"]]
    if update.message is None:
        return ConversationHandler.END
    await update.message.reply_text(
        "Hello! I am WanderBuddy, here to help you with all your travel needs!\n"
        "Send /cancel to stop talking to me.\n\n"
        "Do you want to start a new trip?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )

    return NEW_TRIP

async def new_trip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message and update.message.text == "Yes"):
        chat_id = update.message.chat_id
        logger.info("Chat of id %s started a new trip", chat_id)
        
        await update.message.reply_text(
            "Sure! How many locations will you be going to?\n"
            "Please enter a number.\n\n"
            "For example, if you're flying off to Spain, and then Portugal, please enter '2'.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return LOCATION_COUNT
    else:
        return ConversationHandler.END

async def add_attraction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message and update.message.venue):
        venue = update.message.venue
        chat_id = update.message.chat_id
        logger.info("Chat of id %s added a new attraction %s", chat_id, venue.title)
        latitude, longitude = venue.location.latitude, venue.location.longitude
        
        await update.message.reply_text(
            "Added {} to your trip!".format(venue.title),
            reply_markup=ReplyKeyboardRemove(),
        )
        return ATTRACTION
    else:
        logger.info("Chat of id %s did not add a new attraction", update.message.chat_id)
        return ConversationHandler.END

async def location_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user for locations"""
    await context.bot.send_message(chat_id=update.effective_chat.id or '', text="Wow! {} locations!".format(update.message.text)) 
    
    return ATTRACTION

    # TODO: Continue the conversation by getting all the locations and inserting to DB
    # return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation"""
    chat_id = update.effective_chat.id or ''
    logger.info("Chat of id %s canceled the conversation", chat_id)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download()
    
    update.message.reply_text("Image received")
    
def main():
    load_dotenv()

    # Setup Database
    create_tables()
    db.connect() # alternatively consider connecting to db with each request
    
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(BOT_TOKEN or '').build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NEW_TRIP:[MessageHandler(filters.Regex("^(Yes|No)$"), new_trip)],
            LOCATION_COUNT:[MessageHandler(filters.Regex(r"^\d+$"), location_count)],
            ATTRACTION:[MessageHandler(filters.VENUE, add_attraction)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(conv_handler)
    application.add_handler(unknown_handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()
