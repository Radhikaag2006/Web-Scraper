from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import time

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options = options)
    return driver

# product URL 
product_url = ( "https://www.amazon.in/Dell-i5-1334U-Anti-Glare-Vostro-3530/dp/B0D2Y1BLDT")
driver = get_driver()

print("Opening product page...")
driver.get(product_url)

#Wait for page to fully load
time.sleep(5)
html = driver.page_source
print(f"HTML Length : {len(html)}")
soup = BeautifulSoup(html,"lxml")

# printing the product title 
title = None 
title_tag = soup.find(id  = "productTitle")

if title_tag:
    title = title_tag.get_text(strip = True)
    print("\n"+"=" *  80)
    print("TITLE:")
    print(title)

# price
price = None 
price_tag =  soup.select_one(
      "span.a-price span.a-offscreen")
if price_tag:
    price = price_tag.get_text(strip = True)

print("\n PRICE: ")
print(price)

# specifications table 
print("SPECIFICATIONS")
print("\n")

specifications = {}

spec_table = soup.select_one("table.a-normal.a-spacing-micro")

if spec_table:
    rows = spec_table.find_all("tr")

    for row in rows :
        key_tag = row.find("span", class_="a-text-bold")
        value_tag = row.find("span",class_ = "po-break-word")

        if key_tag and value_tag:

            key = key_tag.get_text(strip = True)
            value = value_tag.get_text(strip = True)
            specifications[key] = value
            print(f"{key}  : {value}")
# image url 
image_url = None
img_tag = soup.find(id = "landingImage")

if img_tag:

    image_url =  img_tag.get("src")
print("\n")
print("Image URL: ")
print(image_url)

# saving html for debugging 
with open("product_page.html","w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("\n Saved product_page.html")
driver.quit()