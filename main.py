import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "JDA0Q93MLIZ3V08J"
NEWS_API_KEY = "82af82da7dd5426591ebddae6b284ef0"
TWILIO_SID = "ACfda5a352ecd167ec3860be423cc2ae34"
TWILIO_AUTH_TOKEN = "1ac25c444f410e8ca9ee04102785514c"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# Find the positive difference between 1 and 2, e.g. 40 - 20 = -20 ...
difference = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# The percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)


# If difference percentage is greater than 2 then print ("Get News").
if abs(diff_percent) > 2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]
    print(three_articles)
    #     print("Get News")
    # else:
    #     print("Ain't A Good News!")

    # Create a new list of the first 3 articles's title and description to your phone number and send via Twilio.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']} \nBrief: {article['description']}" for article in
                          three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+19856038679",
            to="+2348172729632"
        )

