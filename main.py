import asyncio
import json
import logging
import subprocess
import os
import telegram
from requests_oauthlib import OAuth1Session
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from tweepy import OAuthHandler, API

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

try:
    with open("config.json", "r") as f:
        config = json.load(f)
        TELEGRAM_BOT_TOKEN = config["telegram_bot_token"]
        ADMIN_CHAT_ID = config["admin_chat_id"]
        NEWS_FETCHER_SCRIPT = config["news_fetcher_script"]
        X_CONSUMER_KEY = config["x_consumer_key"]
        X_CONSUMER_SECRET = config["x_consumer_secret"]
        X_ACCESS_TOKEN = config["x_access_token"]
        X_ACCESS_TOKEN_SECRET = config["x_access_token_secret"]
        X_CLIENT_ID = config["x_client_id"]
        X_CLIENT_SECRET = config["x_client_secret"]
except FileNotFoundError:
    logger.error("config.json not found. Please create it.")
    exit()
except KeyError as e:
    logger.error(f"Missing key in config.json: {e}")
    exit()
except json.JSONDecodeError:
    logger.error("Invalid JSON in config.json.")
    exit()

def fetch_news():
    try:
        result = subprocess.run(["python", NEWS_FETCHER_SCRIPT], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            with open("news_articles.json", "r") as f:
                return json.load(f)
        else:
            logger.error(f"Error fetching news: {result.stderr}")
            return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Subprocess error: {e}")
        return None
    except FileNotFoundError:
        logger.error(f"File not found: {NEWS_FETCHER_SCRIPT}")
        return None
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from news_articles.json. Check if the file is valid JSON.")
        return None
    except FileNotFoundError:
        logger.error("news_articles.json not found. Check if fetch_news.py is generating it correctly.")
        return None

def post_to_x(filename):
    """Posts the approved article to X (Twitter) using credentials from config.json.

    Args:
        filename (str): Name of the JSON file containing article data.

    Returns:
        bool: True if the post is successful, False otherwise.
    """

    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            consumer_key = config["x_consumer_key"]
            consumer_secret = config["x_consumer_secret"]

        if not os.path.exists(filename):
            logger.error(f"Error: JSON file {filename} not found.")
            return False

        with open(filename, "r") as f:
            article = json.load(f)

        tweet_message = f"{article['title']} \n Read More:{article['url']}"[:280]

        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=config["x_access_token"],
            resource_owner_secret=config["x_access_token_secret"],
        )

        url = "https://api.twitter.com/2/tweets"
        headers = {"Content-Type": "application/json"}
        payload = {"text": tweet_message}

        response = oauth.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            print(f"Posted to X: {tweet_message}")
            return True
        else:
            logger.error(f"Error posting to X: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        logger.error(f"Error posting to X: {e}")
        return False
    

async def send_news_for_approval(context: ContextTypes.DEFAULT_TYPE, articles, current_index=0):
    if not articles:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text="No articles to approve.")
        return

    if current_index >= len(articles):
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text="All articles reviewed.")
        return

    article = articles[current_index]
    message = f"{article['title']}\n\n{article['description']}\n\n[Read More]({article['url']})"  

    keyboard = [
        [
            InlineKeyboardButton("Approve", callback_data=f"approve_{current_index}"),
            InlineKeyboardButton("Reject", callback_data=f"reject_{current_index}"),
        ],
        [InlineKeyboardButton("Approve All", callback_data="approve_all")],
        [InlineKeyboardButton("Reject All", callback_data="reject_all")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message, reply_markup=reply_markup) 
    except telegram.error.BadRequest as e:
        logger.error(f"Error sending message (Bad Request): {e}. Message: {message}")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Error sending message: {e}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    articles = fetch_news()
    if not articles:
        await query.edit_message_text(text="Error fetching news!")
        return
    
    data = query.data
    if data == "approve_all":
        await query.edit_message_text(text="All articles approved!")
        for article in articles:
            if post_to_x(article):
                print(f"Approved and posted: {article['title']}")
            else:
                print(f"Approved but failed to post: {article['title']}")
        return
    elif data == "reject_all":
        await query.edit_message_text(text="All articles rejected.") 
        return

    action, article_index = data.split("_")
    article_index = int(article_index)

    if action == "approve":
        article = articles[article_index]
        try:
            filename = f"approved_article_{article_index}.json"  
            with open(filename, "w") as f:
                json.dump(article, f, indent=4) 
            print(f"Article saved to {filename}")

            if post_to_x(filename):  
                await query.edit_message_text(text=f"Article {article_index + 1} approved and posted to X!")
            else:
                await query.edit_message_text(text=f"Article {article_index + 1} approved, but failed to post to X.")

        except Exception as e:
            logger.error(f"Error saving article to JSON: {e}")
            await query.edit_message_text(text=f"Article {article_index + 1} approved, but there was an error saving the article.")

    elif action == "reject":
        article = articles[article_index]
        await query.edit_message_text(text=f"Article {article_index + 1} rejected!") 
        print(f"Rejected: {article['title']}")

    else:
        await query.edit_message_text(text="Invalid action.") 
        return

    await send_news_for_approval(context, articles, article_index + 1)

async def fetch_new_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = fetch_news()
    if articles:
        await send_news_for_approval(context, articles)
        await update.message.reply_text("News fetched! Awaiting your approval.")
    else:
        await update.message.reply_text("Error fetching news!")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    try:
        await update.message.reply_text("An error occurred. Please try again later.")
    except AttributeError:
        logger.error("Update object has no message attribute. Likely a non-message update.")
    except telegram.error.BadRequest as e:
        logger.error(f"Telegram Bad Request Error in error handler: {e}")


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("fetch", fetch_new_news))
    application.add_handler(CallbackQueryHandler(handle_approval))
    application.add_error_handler(error_handler)

    print(f"Bot started!")
    application.run_polling()
