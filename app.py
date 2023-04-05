import os
import logging
import requests
import threading
from slack_bolt import App
from dotenv import load_dotenv
import schedule
import time
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

# Define the Slack bot token and channel ID
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

# Create an instance of the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Define the API endpoint URL and request data
url = "https://scrapinvest-heohyunjun.koyeb.app/scrape"
api_key = os.environ.get("API_KEY")
data = {
    'url': 'https://www.investing.com/news/stock-market-news',
    'selector': '#leftColumn > div.largeTitle'
}

# Define a function to scrape data and send it to Slack
def scrape_data_and_send_to_slack():
    print("start scraping")
    # Send a POST request to the API endpoint with the data in the request body
    response = requests.post(url, json=data, headers={'api-key': api_key})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the scraped data from the response body
        scraped_data = response.json()

        # Send a message to the Slack bot with the scraped data
        app.client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=f"The scraped data is: {scraped_data}")
    else:
        # Print the error message if the request was not successful
        app.client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=f"Request failed with status code {response.status_code}: {response.text}")

# Schedule the function to run every 10 minutes
schedule.every(10).minutes.do(scrape_data_and_send_to_slack)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

def run_flask_app():
    flask_app.run()

def run_schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Create and start separate threads for the Flask app and the scheduled function loop
    flask_app_thread = threading.Thread(target=run_flask_app)
    schedule_loop_thread = threading.Thread(target=run_schedule_loop)

    flask_app_thread.start()
    schedule_loop_thread.start()

    flask_app_thread.join()
    schedule_loop_thread.join()
