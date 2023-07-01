import telebot
import shazamio

# Telegram Bot Token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Create an instance of the bot
bot = telebot.TeleBot(TOKEN)

# Handler for the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Welcome to the Music Finder Bot! Please enter a song or artist name.")

# Handler for text messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text

    # Call Shazam API to search for the song
    try:
        api = shazamio.Shazam()
        res = api.search(query)

        if res['tracks']['hits']:
            # Get the first matching track
            track = res['tracks']['hits'][0]['track']

            title = track['title']
            artist = track['subtitle']
            url = track['url']

            # Compose the response message
            response_message = f"Here's a matching song:\n\nTitle: {title}\nArtist: {artist}\nURL: {url}"

            # Send the response to the user
            bot.reply_to(message, response_message)
        else:
            bot.reply_to(message, "Sorry, no matching songs found.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred while searching for the song: {e}")

# Start the bot
bot.polling()
