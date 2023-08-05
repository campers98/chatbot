import logging
import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global dictionary to map moods to gifs or stickers
mood_responses = {
    'love': 'https://example.com/love_gif',
    'sad': 'https://example.com/sad_gif',
    # Add more moods and their corresponding gif/sticker URLs here
}

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a message with your mood, and I'll respond with a gif or sticker!")

def handle_message(update: Update, _: CallbackContext) -> None:
    message_text = update.message.text.lower()
    if message_text in mood_responses:
        mood_url = mood_responses[message_text]
        update.message.reply_animation(mood_url)
    else:
        update.message.reply_text("Sorry, I don't recognize that mood. Try 'love' or 'sad'.")

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with the actual bot token obtained from the BotFather
    updater = Updater("YOUR_BOT_TOKEN")

    dispatcher = updater.dispatcher
    # Add command handler to respond to the '/start' command
    dispatcher.add_handler(CommandHandler("start", start))

    # Add message handler to respond to user messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
