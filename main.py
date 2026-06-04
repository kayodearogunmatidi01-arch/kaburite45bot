import os
import telebot

# Retrieve the bot token from Render's environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

bot = telebot.TeleBot(BOT_TOKEN)

# This handler responds to anyone who sends the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "Welcome! I'm glad you're here.\n\n"
        "Use the menu below to get started, and feel free to explore my features."
    )
    # Sends the message back to the chat that triggered it
    bot.reply_to(message, welcome_message)

if __name__ == "__main__":
    print("Bot is starting up...")
    # infinity_polling keeps the bot running continuously
    bot.infinity_polling()
