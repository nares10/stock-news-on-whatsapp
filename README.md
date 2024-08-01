# Stock and News Alert Application

This application monitors the stock price of a specific company (Tesla Inc in this example) and sends an SMS alert if there is a significant change in the stock price. It also fetches relevant news articles about the company and includes them in the alert.

## Features

- Monitors the stock price of Tesla Inc.
- Calculates the percentage change in stock price between two consecutive days.
- Sends an SMS alert if the stock price change is greater than or equal to 5%.
- Fetches and includes the top 3 news articles about Tesla Inc. in the SMS alert.

## Prerequisites

- Python 3.x
- An account with [Alpha Vantage](https://www.alphavantage.co/support/#api-key) to get the stock price data.
- An account with [News API](https://newsapi.org/register) to fetch news articles.
- An account with [Twilio](https://www.twilio.com/) to send SMS alerts.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/nares10/stock-news-on-whatsapp
    cd https://github.com/nares10/stock-news-on-whatsapp
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and add your API keys and phone numbers:
    ```env
    NEWS_API_KEY=your_news_api_key
    ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    FROM_PHONE_NUMBER=your_twilio_phone_number
    TO_PHONE_NUMBER=your_phone_number
    ```

## Usage

Run the application:
```sh
python main.py
```

## How It Works

1. **Setup Logging**: Configures logging to display information and error messages.

2. **Load Environment Variables**: Loads API keys and phone numbers from the `.env` file.

3. **Validate Environment Variables**: Checks if all required environment variables are set.

4. **Get Dates**: Gets the dates for yesterday and the day before yesterday.

5. **Get Stock Data**: Fetches stock data for Tesla Inc. from Alpha Vantage.

6. **Calculate Percentage Change**: Calculates the percentage change in stock price between the two dates.

7. **Get News**: Fetches the top 3 news articles about Tesla Inc. from News API.

8. **Send SMS Alert**: Sends an SMS alert with the stock price change and news articles if the percentage change is greater than or equal to 5%.

## Logging

The application uses Python's built-in logging module to log information and error messages. The logs are displayed in the following format:
```
YYYY-MM-DD HH:MM:SS,sss - LEVEL - MESSAGE
```

## Error Handling

The application includes basic error handling for API requests and message sending. If any required environment variables are missing or if an error occurs during API requests or message sending, appropriate error messages are logged.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Alpha Vantage](https://www.alphavantage.co/) for stock data.
- [News API](https://newsapi.org/) for news articles.
- [Twilio](https://www.twilio.com/) for SMS alerts.

---
