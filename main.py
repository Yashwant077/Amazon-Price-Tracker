import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

# Get this url for any of the product from amazon website
url = os.getenv('amazon_product_url')

# Get this header information using http://myhttpheader.com/ in your browser
header = {
    "User-Agent": os.getenv("MY_USER_AGENT"),
    "Accept-Language": os.getenv("MY_ACCEPT_LANGUAGE")
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

price_text = soup.find("span", class_="a-price-whole").get_text().split(".")[0]
print(price_text)
price_as_int = 0
for char in price_text:
    if '0' <= char <= '9':
        price_as_int = price_as_int * 10 + int(char)
print(price_as_int)

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 30000

if price_as_int < BUY_PRICE:
    message = f"{title} is now available at {price_as_int}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(os.getenv('MY_EMAIL'), os.getenv('MY_PASSWORD'))
        connection.sendmail(
            from_addr=os.getenv('MY_EMAIL'),
            to_addrs=os.getenv('MY_EMAIL'),
            msg=f"Subject:Amazon Price Drop Alert!\n\n{message}\n{url}"
        )
