import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_APIKEY = "YOUR_STOCK_API_KEY"
NEWS_APIKEY = "YOUR_NEWS_API_KEY"
account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'


stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_APIKEY
}

#yesterday stock price
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#differnce 
difference = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#differnce percentage
diff_percentage = round((difference/float(yesterday_closing_price))*100)
print(diff_percentage)

if abs(diff_percentage) >= 1:
    news_params = {
        "apiKey": NEWS_APIKEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params = news_params)
    article = news_response.json()["articles"]
    print(article)

    three_article = article[:3]
    print(three_article)

    #formatting t he article
    formatted_article = [f"{STOCK_NAME}: {up_down}{diff_percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_article]


    client = Client(account_sid, auth_token)
    
    #add your number
    for article in formatted_article:
        message = client.messages.create(
        from_='whatsapp: 000000000000',
        body=article,
        to='whatsapp:0000000000'
        )



