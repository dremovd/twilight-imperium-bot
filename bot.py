import logging
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from secret import token

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Constants
MIN_PLAYERS = 3
MAX_PLAYERS = 6
RACES = ["Race1", "Race2", "Race3"]  # Add all 27 races here

# Global variables
participants = {}
groups = []
admin_user = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global admin_user
    admin_user = update.effective_user.id
    await update.message.reply_text("Welcome to the Board Game Bot! Participants can join by using /join.")


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id not in participants:
        participants[user.id] = {'username': user.username, 'race': None}
        await update.message.reply_text(f"{user.username} has joined the game!")
    else:
        await update.message.reply_text(f"{user.username}, you are already participating!")


def divide_groups():
    global groups
    players = list(participants.values())
    random.shuffle(players)
    groups = [players[i:i + MAX_PLAYERS] for i in range(0, len(players), MAX_PLAYERS)]


async def randomize_races(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    divide_groups()
    for group in groups:
        for player in group:
            choices = random.sample(RACES, 4)
            keyboard = [[InlineKeyboardButton(race, callback_data=f'{player["username"]}:{race}') for race in choices]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f"{player['username']}, choose your race:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    username, race = query.data.split(':')
    for player in participants.values():
        if player['username'] == username:
            player['race'] = race
            await query.edit_message_text(text=f"{username} has selected {race}!")
            break


async def results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = "Final Results:\n"
    for group in groups:
        msg += "Group:\n"
        for player in group:
            msg += f"- {player['username']}: {player['race']}\n"
    await update.message.reply_text(msg)


def main() -> None:
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("join", join))
    application.add_handler(CommandHandler("randomize", randomize_races))
    application.add_handler(CommandHandler("results", results))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
