from scraper.selenium_driver import get_driver
from scraper.search_scraper import scrape_search_page
from scraper.product_scraper import scrape_product_page

driver = get_driver()

products = scrape_search_page(
    driver,
    "laptop",
    page=1
)

first_product = products[0]

details = scrape_product_page(
    driver,
    first_product["product_url"]
)

merged = {
    **first_product,
    **details
}

for key, value in merged.items():
    print(f"{key}: {value}")

driver.quit()