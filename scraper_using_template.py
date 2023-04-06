import os
import requests
import schedule
import datetime
import time

from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()

# Define the Slack bot token and channel ID
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

# Define the API endpoint URL and request data
url = os.environ.get("API_URL")
api_key = os.environ.get("API_KEY")

# Create an instance of the Slack app
app = App(token=SLACK_BOT_TOKEN)

data = {
    'url': 'https://www.investing.com/news/stock-market-news',
    'selector': os.environ.get("SELECTOR")
}

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

# Define a function to scrape data and send it to Slack
def scrape_data_and_send_to_slack():
    print("start scraping")
    response = requests.post(url, json=data, headers={'api-key': api_key})

    if response.status_code == 200:
        scraped_data = response.json()
        current_time = get_current_time()
        blocks = []
        
        # Iterate through the scraped data and build blocks for each article
        for article in scraped_data:
            title = article['title']
            paragraphs = "\n".join(article['paragraphs'])

            # Add a section block with the article title and date
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{title}*\n{current_time}"
                }
            })

            # Add a section block with the article paragraphs
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": paragraphs
                }
            })

            # Add a divider block for visual separation
            blocks.append({
                "type": "divider"
            })

        # Send a message to the Slack bot with the blocks
        app.client.chat_postMessage(
            channel=SLACK_CHANNEL_ID, 
            text="Scraped data summary", 
            blocks=blocks
        )
    else:
        app.client.chat_postMessage(
            channel=SLACK_CHANNEL_ID, 
            text=f"Request failed with status code {response.status_code}: {response.text}"
        )

# Schedule the function to run every 10 minutes
schedule.every(10).minutes.do(scrape_data_and_send_to_slack)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
