import logging
import os
import spacy
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize spaCy NLP models
nlp_en = spacy.load('en')
nlp_ta = spacy.load('ta')
nlp_te = spacy.load('te')

# Telegram Bot API token
TELEGRAM_TOKEN = ''

# Initialize the Telegram updater and dispatcher
updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

# Define a function to detect the language of a text using spaCy
def detect_language(text):
    doc = nlp_en(text)
    if doc._.language['language'] == 'en':
        return 'en'
    
    doc = nlp_ta(text)
    if doc._.language['language'] == 'ta':
        return 'ta'
    
    doc = nlp_te(text)
    if doc._.language['language'] == 'te':
        return 'te'
    
    # Default to English if the language is not detected
    return 'en'

# Define a function to generate responses based on the detected language
def generate_response(text, language):
    if language == 'en':
        return "You said in English: " + text
    elif language == 'ta':
        return "தமிழில் நீங்கள் சொல்லியது: " + text
    elif language == 'te':
        return "మీరు తెలుగులో చెప్పారు: " + text
    else:
        return "Sorry, I cannot understand the language you used."

# Define a function to handle incoming messages
def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_message = update.message.text

    # Detect the language of the incoming message
    detected_language = detect_language(user_message)

    # Generate a response based on the detected language
    response = generate_response(user_message, detected_language)

    # Send the response back to the user
    context.bot.send_message(chat_id=user_id, text=response)

# Register the message handler with the dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_polling()
    updater.idle()
