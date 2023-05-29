import os
import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler,
                          ConversationHandler,
                          MessageHandler, filters)
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
from db import image, supabase

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

NEW_TRIP, NAME_TRIP, SELECT_TRIP, NEW_ROUTE, NAME_ROUTE, SELECT_ROUTE, ADD_ATTRACTION, SHARE_TRIP = range(8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user if they want to start new trip."""
    reply_keyboard =[["Yes", "No"]]
    chat_id = update.message.chat_id
    if update.message is None:
        return ConversationHandler.END
    data, count = supabase.table('trip').select("*", count="exact").eq('user_id', chat_id).range(0, 5).execute()
    data = data[1]
    if len(data) == 0:
        await update.message.reply_text(
            "Hello! I am WanderBuddy, here to help you with all your travel needs!\n"
            "Send /cancel to stop talking to me.\n\n"
            "Do you want to start a new trip?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True
            ),
        )
        return NEW_TRIP
    else:
        content_string = '\n'.join(['{}. {}'.format(index + 1, trip['name']) for index, trip in enumerate(data)])
        markup_buttons = [
            InlineKeyboardButton(str(index + 1), callback_data='select#{}'.format(data[index]['id']))
            for index in range(len(data))
        ]
        if count[1] > 5:
            markup_buttons.append(InlineKeyboardButton(">>", callback_data='page#{}'.format(1)))
            await update.message.reply_text(
                "Welcome back to WanderBuddy\n" +
                "Send /cancel to stop talking to me.\n\n" +
                "Here are a list of your trips:\n" + 
                content_string + "\n\n" +
                "Which trip do you want to select?",
                reply_markup=InlineKeyboardMarkup([markup_buttons]),
                parse_mode="Markdown"
            )

        return SELECT_TRIP

async def select_trip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    command = query.data.split('#')[0]
    if command == "select":
        trip_id = int(query.data.split('#')[1])
        data, count = supabase.table('trip').select("*").eq('id', trip_id).execute()
        context.user_data["current_trip"] = data[1][0]['id']
        await context.bot.send_message(
            chat_id=chat_id,
            text="{} has been selected as the current trip!\n".format(data[1][0]['name'])
        )
        return await new_route(update, context)

    elif command == "page":
        page = int(query.data.split('#')[1])
        data, count = supabase.table('trip').select("*", count="exact").eq('user_id', chat_id).range(page * 5, page * 5 + 5).execute()
        data = data[1]
        count = count[1]
        content_string = '\n'.join(['{}. {}'.format(page * 5 + index + 1, trip['name']) for index, trip in enumerate(data)])
        markup_buttons = [
            InlineKeyboardButton(str(page * 5 + index + 1), callback_data='select#{}'.format(data[index]['id']))
            for index in range(len(data))
        ]

        if count > page * 5 + 4:
            markup_buttons.append(InlineKeyboardButton(">>", callback_data='page#{}'.format(page + 1)))
        if page > 0:
            markup_buttons.insert(0, InlineKeyboardButton("<<", callback_data='page#{}'.format(page - 1)))

        await query.edit_message_text(
            text="Here are a list of your trips:\n" + content_string 
                + "\n\nWhich trip do you want to select?",
            reply_markup=InlineKeyboardMarkup([markup_buttons]),
            parse_mode='markdown'
        )
        return SELECT_TRIP
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

        data, count = supabase.table('trip').insert({"name": update.message.text, "user_id": chat_id}).execute()
        context.user_data["current_trip"] = data[1][0]['id']
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
    current_trip = context.user_data.get("current_trip", -1)
    if current_trip == -1:
        return -1
    data, count = supabase.table('route').select("*", count="exact").eq('trip', current_trip).range(0, 5).execute()
    data = data[1]
    chat_id = update.callback_query.message.chat_id

    if len(data) == 0:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Shall we start by creating a new route?\n\nWhat shall we call your new route?",
            reply_markup=ReplyKeyboardRemove()
        )
        return NAME_ROUTE
            
    else:
        content_string = '\n'.join(['{}. {}'.format(index + 1, route['name']) for index, route in enumerate(data)])
        markup_buttons = [
            InlineKeyboardButton(str(index + 1), callback_data='select#{}'.format(data[index]['id']))
            for index in range(len(data))
        ]
        if count[1] > 5:
            markup_buttons.append(InlineKeyboardButton(">>", callback_data='page#{}'.format(1)))
        await context.bot.send_message(
            chat_id=chat_id,
            text="Here are a list of your routes:\n" + 
            content_string + "\n\n" +
            "Which route do you want to select?",
            reply_markup=InlineKeyboardMarkup([markup_buttons]),
            parse_mode="Markdown"
        )

        return SELECT_ROUTE

async def select_route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    command = query.data.split('#')[0]
    if command == "select":
        route_id = int(query.data.split('#')[1])
        data, count = supabase.table('route').select("*").eq('id', route_id).execute()
        context.user_data["current_route"] = data[1][0]['id']
        await context.bot.send_message(
            chat_id=chat_id,
            text="{} has been selected as the current route!\n".format(data[1][0]['name'])
        )
        return SELECT_ROUTE

    elif command == "page":
        trip_id = update.user_data.get("current_trip", -1)
        if trip_id == -1:
            return -1
        page = int(query.data.split('#')[1])
        data, count = supabase.table('route').select("*", count="exact").eq('trip', trip_id).range(page * 5, page * 5 + 5).execute()
        data = data[1]
        count = count[1]
        content_string = '\n'.join(['{}. {}'.format(page * 5 + index + 1, trip['name']) for index, trip in enumerate(data)])
        markup_buttons = [
            InlineKeyboardButton(str(page * 5 + index + 1), callback_data='select#{}'.format(data[index]['id']))
            for index in range(len(data))
        ]

        if count > page * 5 + 4:
            markup_buttons.append(InlineKeyboardButton(">>", callback_data='page#{}'.format(page + 1)))
        if page > 0:
            markup_buttons.insert(0, InlineKeyboardButton("<<", callback_data='page#{}'.format(page - 1)))

        await query.edit_message_text(
            text="here are a list of your trips:\n" + content_string 
                + "\n\nwhich trip do you want to select?",
            reply_markup=InlineKeyboardMarkup([markup_buttons]),
            parse_mode='markdown'
        )
        return SELECT_ROUTE

async def name_route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message and update.message.text):
        chat_id = update.message.chat_id
        logger.info("Chat of id %s started a new route named %s", chat_id, update.message.text)

        # TODO: Add route to DB
        current_trip = context.user_data.get("current_trip")
        data, count = supabase.table('route').insert({ "trip": current_trip, "name": update.message.text }).execute()
        if "current_routes" not in context.user_data:
            context.user_data["current_routes"] = {}
        context.user_data["current_routes"][data[1][0]['id']] = 0 # {rout_id: location_index}
        context.user_data["current_route_id"] = data[1][0]['id']

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
        venue = update.message.venue
        chat_id = update.message.chat_id
        logger.info("Chat of id %s added a new attraction %s", chat_id, venue.title)
        latitude, longitude = venue.location.latitude, venue.location.longitude
        
        # insert into db (trigger prevents duplicate insertions)
        new_location = {"name": venue.title, "lat": latitude, "lng": longitude}
        location_id = -1
        try:
            data, count = supabase.table('location').insert(new_location).execute()
            location_id = data[1][0]['id']
            logger.info(f"Location id {location_id}")
        except: 
            logger.info(f"Duplicate location detected")
            data, count = supabase.table('location').select("*").match(new_location).execute()
            location_id = data[1][0]['id']
            logger.info(f"Location id {location_id}")
        
        context.user_data["current_routes"][context.user_data["current_route_id"]] += 1
        new_route_loc ={'route_id': context.user_data["current_route_id"], "location_id": location_id, "index": context.user_data["current_routes"][context.user_data["current_route_id"]]} 

        try:
            data, count = supabase.table('route_has_location').insert(new_route_loc).execute()
            logger.info(f"Route location added to db: {data}")
        except:
            logger.info(f"Duplicate route location detected")
            data, count = supabase.table('route_has_location').select("*").match(new_route_loc).execute()
            logger.info(f"Route location added to db: {data}")

        await update.message.reply_text(
            "Added {} to your trip!\n\n".format(venue.title) +
            "You can continue adding other attractions to your route, just send me the venues!",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ADD_ATTRACTION
    else:
        logger.info("Chat of id %s did not add a new attraction", update.message.chat_id)
        return ADD_ATTRACTION

async def share_trip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    command = "/share_trip"
    if (update.message and update.message.text.startswith(command)):
        usernames = update.message.text[len(command) + 1:].split(" ")
        chat_id = update.message.chat_id
        try:
            trip_id = supabase.table('trip').select('id').match({
                'id': context.user_data["current_trip"],
                'user_id': chat_id
            }).execute().data[0]['id']
        except:
            logger.warning("Chat of id %s tried to share a trip that does not exist", chat_id)
            
        logger.info("Chat of id %s shared trip of id %s with %s", chat_id, trip_id, ", ".join(usernames))
        
        for user in usernames:
            data, count = supabase.table('shared_trips').insert({"trip_id": trip_id, "user_id": user}).execute()
            logger.info(f"Shared trip with {user} added to db: {data}")
        
        await update.message.reply_text(
            "Shared trip of id {} with {}!\n\n".format(context.user_data["current_trip"], ", ".join(usernames)),
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
        
    elif (update.message is not None):
        await update.message.reply_text("Sorry! I can't read those username(s), please try again!\n")
        return ConversationHandler.END
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
        per_user=False,
        entry_points=[CommandHandler("start", start)],
        states={
            NEW_TRIP:[MessageHandler(filters.Regex("^(Yes|No)$"), new_trip)],
            NAME_TRIP:[MessageHandler(filters.TEXT, name_trip)],
            SELECT_TRIP:[CallbackQueryHandler(select_trip, pattern='^(page|select)#')],
            NEW_ROUTE:[MessageHandler(filters.Regex("^(Yes|No)$"), new_route)],
            NAME_ROUTE:[MessageHandler(filters.TEXT, name_route)],
            SELECT_ROUTE:[CallbackQueryHandler(select_route, pattern='^(page|select)#')],
            ADD_ATTRACTION:[MessageHandler(filters.VENUE, add_attraction)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    share_trip_handler = CommandHandler("share_trip", share_trip)
    image_handler = MessageHandler(filters.PHOTO, image)
    
    application.add_handler(conv_handler)
    application.add_handler(share_trip_handler)
    application.add_handler(unknown_handler)
    application.add_handler(image_handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()
