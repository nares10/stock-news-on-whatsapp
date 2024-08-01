from dotenv import load_dotenv
import os
import requests
import datetime as dt
import logging
from twilio.rest import Client

# Constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_URL = "https://www.alphavantage.co/query"
NEWS_API_URL = "https://newsapi.org/v2/everything"
DATE_FORMAT = "%Y-%m-%d"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
FROM_PHONE_NUMBER = os.getenv('FROM_PHONE_NUMBER')
TO_PHONE_NUMBER = os.getenv('TO_PHONE_NUMBER')

# Validate environment variables
required_env_vars = [NEWS_API_KEY, ALPHA_VANTAGE_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN]
if any(var is None for var in required_env_vars):
    raise ValueError("One or more required environment variables are missing.")

def get_dates():
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=1)
    day_before_yesterday = today - dt.timedelta(days=2)
    return yesterday.strftime(DATE_FORMAT), day_before_yesterday.strftime(DATE_FORMAT)

def get_stock_data(stock, api_key):
    params = {
        'function': "TIME_SERIES_DAILY",
        'symbol': stock,
        'apikey': api_key,
    }
    response = requests.get(STOCK_API_URL, params=params)
    if response.status_code != 200:
        logging.error("Error fetching stock data.")
        return None
    return response.json().get('Time Series (Daily)', {})

def calculate_percentage_change(yesterday_data, day_before_yesterday_data):
    try:
        yesterday_close = float(yesterday_data['4. close'])
        day_before_yesterday_close = float(day_before_yesterday_data['4. close'])
        return ((yesterday_close - day_before_yesterday_close) / day_before_yesterday_close) * 100
    except KeyError as e:
        logging.error(f"Error calculating percentage change: {e}")
        return None

def get_news(company_name, from_date, api_key):
    params = {
        'q': company_name,
        'from': from_date,
        'sortBy': "popularity",
        'apiKey': api_key,
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code != 200:
        logging.error("Error fetching news data.")
        return []
    return response.json().get('articles', [])[:3]

def send_message_about_news(account_sid, auth_token, message):
    client = Client(account_sid, auth_token)
    try:
        client.messages.create(
            from_=FROM_PHONE_NUMBER,
            body=message,
            to=TO_PHONE_NUMBER
        )
        logging.info("Message sent successfully.")
    except Exception as e:
        logging.error(f"Error sending message: {e}")

def main():
    yesterday, day_before_yesterday = get_dates()
    stock_data = get_stock_data(STOCK, ALPHA_VANTAGE_API_KEY)
    
    if not stock_data:
        return
    
    if yesterday not in stock_data or day_before_yesterday not in stock_data:
        logging.error("Stock data for the required dates is not available.")
        return
    
    percentage_change = calculate_percentage_change(stock_data[yesterday], stock_data[day_before_yesterday])
    
    if percentage_change is None:
        return
    
    logging.info(f"Percentage change: {percentage_change:.2f}%")
    condition = abs(percentage_change) >= 5
    sign = ""
    if percentage_change > 0:
        sign = "+"
    else:
        sign = "-" 

    if True:
        logging.info("Significant change detected. Fetching news...")
        articles = get_news(COMPANY_NAME, yesterday, NEWS_API_KEY)
        for article in articles:
            headline = article.get('title', 'No title')
            description = article.get('description', 'No description')
            news = f"{STOCK}: {sign}{percentage_change:.2f}\nHeadline: {headline}\nBrief: {description}\n"
            send_message_about_news(account_sid=TWILIO_ACCOUNT_SID, auth_token=TWILIO_AUTH_TOKEN, message=news)
    else:
        logging.info("No significant change detected.")

if __name__ == "__main__":
    main()
