import json
import urllib.request

try:
    with open("config.json", "r") as f:
        config = json.load(f)
        print("Config loaded successfully:")
        # print(config)
        NEWS_API_KEY = config["news_api_key"]
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    print(f"Error loading config.json: {e}")
    exit()

apikey = NEWS_API_KEY
category = "nation" #general, world, nation, business, technology, entertainment, sports, science and health.
country = "in"
max = 20
url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country={country}&max={max}&apikey={apikey}"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))
    articles = data["articles"]

# Create a new list to store the formatted data
formatted_articles = []

for article in articles:
    formatted_article = {
        "url": article["url"],
        "title": article["title"],
        "description": article["description"],
        "image": article["image"],
        "content": article["content"],
    }
    formatted_articles.append(formatted_article)

# Save the formatted articles to a JSON file
with open("news_articles.json", "w", encoding="utf-8") as outfile:
    json.dump(formatted_articles, outfile, indent=4)

print("Articles saved to news_articles.json!")
