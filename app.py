import os
from slack_bolt import App
from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

load_dotenv()

# Define the Slack bot token and channel ID
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

# Create an instance of the Slack app
app = App(token=SLACK_BOT_TOKEN)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run()
