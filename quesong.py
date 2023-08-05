import logging
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Update, InputMediaPhoto, InputMediaAnimation
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your Spotify API credentials
SPOTIFY_CLIENT_ID = 'e60cd7a829cc4a80804553a20c216379'
SPOTIFY_CLIENT_SECRET = 'c9d6d953a45b47aea4f56a0acb45ece2'

# Global dictionary to map moods to gifs or stickers
mood_responses = {
    'love': 'https://example.com/love_gif',
    'sad': 'https://example.com/sad_gif',
    'happy': 'https://example.com/happy_gif',
    # Add more moods and their corresponding gif/sticker URLs here
}

def get_song_mood(track_id):
    # Set up the Spotify API client
    auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get the audio features of the track
    audio_features = sp.audio_features(track_id)
    if audio_features and 'valence' in audio_features[0]:
        valence = audio_features[0]['valence']
        if valence > 0.7:
            return 'happy'
        elif valence < 0.3:
            return 'sad'
        else:
            return 'love'
    else:
        # If audio features are not available, assume a neutral mood
        return 'neutral'

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a Spotify track URL, and I'll analyze the mood of the song and respond with a gif or sticker!")

def handle_message(update: Update, _: CallbackContext) -> None:
    # Check if the message contains a Spotify track URL
    if 'open.spotify.com/track/' in update.message.text:
        # Extract the track ID from the URL
        track_id = update.message.text.split('/')[-1].split('?')[0]
        mood = get_song_mood(track_id)
        if mood in mood_responses:
            mood_url = mood_responses[mood]
            update.message.reply_animation(mood_url)
        else:
            update.message.reply_text("Sorry, I couldn't determine the mood of the song.")
    else:
        update.message.reply_text("Please provide a valid Spotify track URL.")

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with the actual bot token obtained from the BotFather
    updater = Updater("6348947600:AAGyq_j6l8HXqT2Go8htNBQceJf1uaLxt4M")

    dispatcher = updater.dispatcher
    # Add command handler to respond to the '/start' command
    dispatcher.add_handler(CommandHandler("start", start))

    # Add message handler to respond to user messages
    dispatcher.add_handler(MessageHandler(~CommandHandler("start"), start))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
