from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def get_driver():

    options = Options()

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    return driver


driver = get_driver()

url = "https://www.amazon.in/s?k=laptop"

driver.get(url)

# wait for page to load
time.sleep(5)

html = driver.page_source

print(f"HTML Length: {len(html)}")

soup = BeautifulSoup(html, "lxml")


product_cards = soup.select('div[data-component-type="s-search-result"]')
with open("first_card.html", "w", encoding="utf-8") as f:
    f.write(product_cards[0].prettify())

print(f"Found {len(product_cards)} cards\n")

count = 0

for card in product_cards:

    asin = card.get("data-asin", "").strip()

    if not asin:
        continue

    title = None
    image_url = None
    product_url = None
    sale_price = None
    mrp  = None

    # title
    h2 = card.find("h2")

    if h2:
        title = h2.get_text(strip=True)

    # image
    img = card.find("img")

    if img:
        image_url = img.get("src")

    # price extraction 
    # sale price 
    sale_price_tag = card.select_one('span.a-price:not(.a-text-price) span.a-offscreen')
    if sale_price_tag:
        sale_price = sale_price_tag.get_text(strip =  True)

    # mrp 
    mrp_tag = card.select_one('span.a-price.a-text-price span.a-offscreen')
    if mrp_tag:
        mrp = mrp_tag.get_text(strip = True)
    # product link
    a_tag = card.find("a", href=True)

    if a_tag:

     href = a_tag["href"]

     sponsored_skipped = 0
    # Skip sponsored products
    if "/sspa/" in href:
        sponsored_skipped += 1
        continue

    
    if href.startswith("/"):
        product_url = (
            "https://www.amazon.in" + href
        )
    else:
        product_url = href

    print("=" * 80)

    print("ASIN:")
    print(asin)

    print("\nTITLE:")
    print(title)

    print("\nPRODUCT URL:")
    print(product_url)

    print("\nIMAGE URL:")
    print(image_url)

    print("\nSALE PRICE:")
    print(sale_price)

    print("\nMRP:")
    print(mrp)

    count += 1

    if count == 5:
        break

print(
    f"\nSponsored products skipped: "
    f"{sponsored_skipped}")
   

driver.quit()