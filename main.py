import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

MY_NUMBER = "NUMBER"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"

Alpha_Vantage_Key = "KEY"

STOCK_PARAMETERS = {"function": "TIME_SERIES_DAILY",
                    "symbol": STOCK_NAME,
                    "datatype": "json",
                    "apikey": Alpha_Vantage_Key,
                    }

TWILO_SID = "SID"
AUTH_TOKEN = "TOKEN"
TWILO_PHONE_NUMBER = "T-NUMBER"

yesterday_raw = datetime.now() - timedelta(1)
yesterday = yesterday_raw.date()

two_days_ago_raw = datetime.now() - timedelta(2)
two_days_ago = two_days_ago_raw.date()

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

GET_NEWS_API = "AIP"

NEWS_PARAMETERS = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "sortBy": "top-headlines",
    "apiKey": GET_NEWS_API,

}


news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
news_response.raise_for_status()
news_data = news_response.json()


stock_response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMETERS)
stock_response.raise_for_status()
stock_data = stock_response.json()

try:
    yesterday_closing = stock_data["Time Series (Daily)"][str(yesterday)]['4. close']

    two_days_ago_closing = stock_data["Time Series (Daily)"][str(two_days_ago)]['4. close']

    stock_change = abs(float(yesterday_closing) - float(two_days_ago_closing))

    percent = stock_change / float(yesterday_closing) * 100

    article = 0
    news_list = []
    is_news = False

    if percent >= 5:
        is_news = True
        while article < 3:
            yesterday_url = news_data['articles'][article]['url']
            yesterday_title = news_data['articles'][article]['title']
            yesterday_description = news_data['articles'][article]['description']
            news_list.append(yesterday_title)
            news_list.append(yesterday_url)
            news_list.append(yesterday_description)
            article += 1

    up_down = ''
    if yesterday_closing > two_days_ago_closing:
        up_down = "🔺"

    elif yesterday_closing < two_days_ago_closing:
        up_down = "🔻"

    if is_news:
        client = Client(TWILO_SID, AUTH_TOKEN)

        news1 = f"{STOCK_NAME}{up_down}\n\n" \
                f"Headline: {news_list[0]}\n\n" \
                f"Link: {news_list[1]}\n\n" \
                f"Brief: {news_list[2]}"
        message1 = client.messages.create(body=news1,
                                          from_=TWILO_PHONE_NUMBER,
                                          to=MY_NUMBER
                                          )

        news2 = f"{STOCK_NAME}{up_down}\n\n" \
                f"Headline: {news_list[3]}\n\n" \
                f"Link: {news_list[4]}\n\n" \
                f"Brief: {news_list[5]}"
        message2 = client.messages.create(body=news2,
                                          from_=TWILO_PHONE_NUMBER,
                                          to=MY_NUMBER
                                          )

        news3 = f"{STOCK_NAME}{up_down}\n\n" \
                f"Headline: {news_list[6]}\n\n" \
                f"Link: {news_list[7]}\n\n" \
                f"Brief: {news_list[8]}"
        message3 = client.messages.create(body=news3,
                                          from_=TWILO_PHONE_NUMBER,
                                          to=MY_NUMBER
                                          )


except KeyError:
    print("Stocks don't update on the weekend")


