# 🚀 Telegram News Approval Bot

A Telegram bot that fetches news articles, allows an admin to approve or reject them, and posts approved articles to X (formerly Twitter). 📰

## ✨ Features
- 📡 Fetches news articles from GNews API.
- 🤖 Sends articles to a Telegram admin for review.
- ✅ Approve or ❌ reject individual articles via inline buttons.
- 🆗 "Approve All" and 🚫 "Reject All" options.
- 🐦 Posts approved articles to X.

## 📌 Prerequisites
- 🐍 Python 3.x
- 🤖 A Telegram bot token
- 🔑 X (Twitter) API credentials
- 🗂️ A `config.json` file with required keys

## 🛠️ Installation

### 🖥️ Windows
1. Clone this repository:
    ```sh
    git clone https://github.com/your-repo/news-telegram-bot.git
    cd news-telegram-bot
    ```
2. Create a virtual environment:
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Create a `config.json` file:
    ```json
    {
      "news_api_key": "YOUR_GNEWS_API_KEY",
      "telegram_bot_token": "YOUR_BOT_TOKEN",
      "admin_chat_id": YOUR_ADMIN_CHAT_ID,
      "news_fetcher_script": "news_fetcher.py",
      "x_consumer_key": "YOUR_X_CONSUMER_KEY",
      "x_consumer_secret": "YOUR_X_CONSUMER_SECRET",
      "x_access_token": "YOUR_X_ACCESS_TOKEN",
      "x_access_token_secret": "YOUR_X_ACCESS_TOKEN_SECRET",
      "x_client_id": "YOUR_X_CLIENT_ID",
      "x_client_secret": "YOUR_X_CLIENT_SECRET"
    }
    ```

### 🐧 Linux / 🍏 macOS
1. Clone this repository:
    ```sh
    git clone https://github.com/your-repo/news-telegram-bot.git
    cd news-telegram-bot
    ```
2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Create a `config.json` file (same as above).

## 🚀 Usage

### 🔧 Start the Bot
Run the bot with:
```sh
python bot.py
```

### 📝 Telegram Commands
- `/fetch` - Fetches and sends news articles for approval.

### 🎛️ Inline Button Actions
- ✅ **Approve** - Approves and posts an article to X.
- ❌ **Reject** - Rejects an article.
- 🆗 **Approve All** - Approves and posts all articles.
- 🚫 **Reject All** - Rejects all articles.

## 🌍 Deployment

To deploy this bot on a server, follow these steps:

1. **Set up a cloud server (e.g., AWS, DigitalOcean, or a VPS).**
2. **Install required packages:**
    ```sh
    sudo apt update && sudo apt install python3 python3-venv
    ```
3. **Clone the repository and navigate to the folder:**
    ```sh
    git clone https://github.com/your-repo/news-telegram-bot.git
    cd news-telegram-bot
    ```
4. **Create a virtual environment and install dependencies:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
5. **Run the bot in the background:**
    ```sh
    nohup python bot.py &
    ```
6. **(Optional) Use a process manager like `systemd` or `screen` for reliability.**

## 📜 License
This project is open-source under the MIT License.

## 👨‍💻 Author

### Pragnesh Singh  
[![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/pragnesh-singh-rajput)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/pragnesh-singh-rajput) 
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?logo=instagram&logoColor=white)](https://instagram.com/pragnesh_singh_rajput)

