# Investing.com News Scraper

This project scrapes the latest news articles from Investing.com and sends them to a designated Slack channel using a bot.

## Setup

1. Clone this repository and navigate to the root directory.
2. Install the required packages using `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory with the following variables:

   ```
   API_URL=<your API endpoint URL>
   API_KEY=<your API key>
   SELECTOR=<your CSS selector>
   SLACK_BOT_TOKEN=<your Slack bot token>
   SLACK_CHANNEL_ID=<your Slack channel ID>
   ```

4. Run the script using `python scraper_using_template.py`.

## How it works

The `scraper_using_template.py` script sends a POST request to the API endpoint with the URL and CSS selector to scrape. The API scrapes the data and returns it as a JSON object. The script then formats the data and sends it to the designated Slack channel using the Slack bot.

The script runs every 10 minutes using the `schedule` package.

## Contributions

Contributions to this project are welcome. To contribute, please fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
