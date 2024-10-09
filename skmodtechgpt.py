import logging
import requests
import asyncio
import nest_asyncio
import os
from telegram import Update  # Import Update here
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Allow nested event loops
nest_asyncio.apply()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your ChatGPT bot. How can I assist you today?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    # Make a request to the API
    response = requests.get(f"https://bj-tricks.serv00.net/BJ_Coder-Apis/gpt4o.php?question={user_message}")

    if response.status_code == 200:
        # Get the reply text from the response
        reply_data = response.json()
        if "message" in reply_data:
            await update.message.reply_text(reply_data["message"].replace('"Credit": "https://t.me/BJ_Tricks"', ''))
    else:
        await update.message.reply_text("Sorry, I couldn't fetch a response.")

async def main() -> None:
    # Use your bot token from an environment variable for security
    my_secret = os.environ['BOT_TOKEN']
    application = ApplicationBuilder().token(my_secret).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

# Entry point for the script
if __name__ == '__main__':
    asyncio.run(main())
