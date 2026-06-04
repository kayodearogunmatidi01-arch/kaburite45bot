import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Enable logging to see what's happening in Render logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Retrieve environment variables from Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI Client
ai_client = OpenAI(api_key=OPENAI_API_KEY)

# Define the system prompt to make the AI act like a real person
SYSTEM_PROMPT = (
    "You are a friendly, casual, and empathetic human chatting on Telegram. "
    "Keep your answers relatively concise, conversational, and natural. "
    "Do not sound like a rigid AI assistant. Use emojis occasionally where appropriate."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a greeting message when the command /start is issued."""
    await update.message.reply_text("Hey there! Great to connect with you. What's on your mind today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming text messages, sends them to OpenAI, and replies to the user."""
    user_text = update.message.text
    
    try:
        # Call the AI API
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7 # Makes the AI a bit more creative and human-like
        )
        
        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)
        
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        await update.message.reply_text("Sorry, I got a bit distracted! Could you say that again?")

def main() -> None:
    """Start the bot."""
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
        logger.error("Missing environment variables! Please set TELEGRAM_TOKEN and OPENAI_API_KEY.")
        return

    # Build the Telegram Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # CRITICAL FOR BACKGROUND WORKERS: Use run_polling instead of webhooks.
    # This continuously requests updates from Telegram directly.
    logger.info("Bot is starting via long polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
