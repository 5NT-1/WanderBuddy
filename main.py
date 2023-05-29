import os
import logging
from dotenv import load_dotenv
from telegram import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          ConversationHandler, InlineQueryHandler,
                          MessageHandler, filters)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

NEW_TRIP, NAME_TRIP, NEW_ROUTE, NAME_ROUTE, ADD_ATTRACTION = range(5)

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
        await update.message.reply_text(
            "What shall we call your new trip?",
            reply_markup=ReplyKeyboardRemove()
        )

        return NAME_TRIP
        
    elif (update.message is not None):
        await update.message.reply_text("Sure! Let me know again with /start whenever you change your mind.\n")
        return ConversationHandler.END

async def name_trip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message):
        chat_id = update.message.chat_id
        logger.info("Chat of id %s started a new trip named %s", chat_id, update.message.text)
        reply_keyboard =[["Yes", "No"]]

        # TODO: Add trip to DB
        
        await update.message.reply_text(
            "Wow! {} sounds like fun! Shall we start by creating a new route?\n".format(update.message.text) + 
            "Each Trip composes of multiple routes. A route is a single adventure of multiple attractions that are near each other!\n\n"
            "For example, a route in Singapore might go from Singapore Flyer, to the Merlion, to the Explanade!.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True
            ),
        )
        return NEW_ROUTE

async def new_route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message and update.message.text == "Yes"):
        await update.message.reply_text(
            "What shall we call your new route?",
            reply_markup=ReplyKeyboardRemove()
        )
        return NAME_ROUTE
        
    elif (update.message is not None):
        await update.message.reply_text("Sure! Let me know again whenever you change your mind.\n")
        return NEW_ROUTE
    return ConversationHandler.END

async def name_route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message and update.message.text):
        chat_id = update.message.chat_id
        logger.info("Chat of id %s started a new route named %s", chat_id, update.message.text)

        # TODO: Add route to DB
        await update.message.reply_text(
            "Great! Let's start by adding our first attraction to {}\n".format(update.message.text) +
            "Simple reply by sending an inline location."
        )
        return ADD_ATTRACTION
    else:
        await update.message.reply_text(
            "Sorry! I can't read that name, please try again!",
            reply_markup=ReplyKeyboardRemove()
        )
        return NAME_ROUTE

async def add_attraction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message and update.message.venue):
        chat_id = update.message.chat_id
        venue = update.message.venue
        
        logger.info("Chat of id %s added a new attraction", chat_id)
        
        await update.message.reply_text(
            "Added {} to your trip!".format(venue.title),
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        logger.info("Chat of id %s did not add a new attraction", update.message.chat_id)
        return ConversationHandler.END



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
    
def main():
    load_dotenv()

    # Setup Database
    
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(BOT_TOKEN or '').build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NEW_TRIP:[MessageHandler(filters.Regex("^(Yes|No)$"), new_trip)],
            NAME_TRIP:[MessageHandler(filters.ALL, name_trip)],
            NEW_ROUTE:[MessageHandler(filters.Regex("^(Yes|No)$"), new_route)],
            NAME_ROUTE:[MessageHandler(filters.ALL, name_route)],
            ADD_ATTRACTION:[MessageHandler(filters.VENUE, add_attraction)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(conv_handler)
    application.add_handler(unknown_handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()
