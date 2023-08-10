# Importing necessary libraries and modules
import logging
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from secret import token
from factions import FACTIONS  # Assuming FACTIONS contains the races data

# Enabling logging for debugging purposes
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants to define the minimum and maximum number of players and factions
MIN_PLAYERS = 2
MAX_PLAYERS = 8
MAX_FACTIONS_TO_SELECT = 4

# Constants
ADMIN_USERNAME = 'dremovd'

# Global variables to store participants and groups information
participants = {}
groups = []
admin_user = None
available_races = []

# Function to check if the user is an admin
def is_admin(username: str) -> bool:
    return username == ADMIN_USERNAME

# Start command to welcome the admin user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global admin_user
    admin_user = update.effective_user.id
    await update.message.reply_text("Welcome to the Board Game Bot! Participants can join by using /join.")

# Join command to allow users to participate in the game
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id not in participants:
        participants[user.id] = {'username': user.username, 'user_id': user.id, 'race': None}  # Include user_id
        logger.info(f"User {user.username} joined with ID {user.id}")
        await update.message.reply_text(f"{user.username} has joined the game!")
    else:
        await update.message.reply_text(f"{user.username}, you are already participating!")

# Function to divide participants into groups
def divide_groups():
    global groups
    players = list(participants.values())
    random.shuffle(players)
    groups = [players[i:i + MAX_PLAYERS] for i in range(0, len(players), MAX_PLAYERS)]

# Command to randomize races and allow users to select their race
async def randomize_races(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.username):
        await update.message.reply_text("Only the admin can randomize races.")
        return
    
    global available_races
    available_races = FACTIONS.copy()
    divide_groups()

    for group in groups:
        for player in group:
            choices = random.sample(available_races, 4)
            # Remove the chosen races from available_races
            available_races = [race for race in available_races if race not in choices]

            # Create the message text with the full names of the races
            message_text = "Choose your race:\n"
            for i, race in enumerate(choices):
                message_text += f"{i + 1}. {race['name']}\n"

            # Create the keyboard with buttons containing numbers corresponding to the races
            keyboard = [[InlineKeyboardButton(str(i + 1), callback_data=f'{player["username"]}:{race["name"]}') for i, race in enumerate(choices)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send the message to the corresponding player
            await context.bot.send_message(chat_id=player['user_id'], text=message_text, reply_markup=reply_markup)

# Function to handle button clicks for race selection
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    username, race = query.data.split(':')
    for player in participants.values():
        if player['username'] == username:
            player['race'] = race
            await query.edit_message_text(text=f"{username} has selected {race}!")
            break

# Command to display the final results
async def results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.username):
        await update.message.reply_text("Only the admin can view results.")
        return
    global participants, groups, available_races

    msg = "Final Results:\n"
    for group in groups:
        msg += "Group:\n"
        for player in group:
            msg += f"- {player['username']}: {player['race']}\n"
    await update.message.reply_text(msg)

    # Clear all stored information
    participants.clear()
    groups.clear()
    available_races.clear()

# Main function to set up the bot commands and start the bot
def main() -> None:
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("join", join))
    application.add_handler(CommandHandler("randomize", randomize_races))
    application.add_handler(CommandHandler("results", results))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Entry point of the script
if __name__ == "__main__":
    main()

