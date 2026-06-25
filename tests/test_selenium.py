from scraper.selenium_driver import get_driver
from scraper.product_scraper import scrape_product_page

driver = get_driver()

url = "https://www.amazon.in/dp/B0D2Y1BLDT"

data = scrape_product_page(
    driver,
    url
)

for key, value in data.items():
    print(f"{key}: {value}")

driver.quit()