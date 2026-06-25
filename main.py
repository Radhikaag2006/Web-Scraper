from scraper.selenium_driver import get_driver
from scraper.search_scraper import scrape_search_page
from scraper.product_scraper import scrape_product_page

import pandas as pd
import os 


def main():

    category = input(
        "Enter category: "
    ).strip()

    driver = get_driver()

    all_search_products = []

    # scraping all 10 search pages 
    for page in range(1,11):
        print(f"\n Scraping Search Page{page}")

        products = scrape_search_page(
            driver,
            category,
            page=1
        )

        all_search_products.extend(products)

        print(
            f"\n Total Products Found: " f"{len(all_search_products)}"
        )

   # removing duplictes
    seen_asins = set()
    unique_products = []

    for product in all_search_products:
        asin = product["asin"]

        if asin in seen_asins:
            continue
        seen_asins.add(asin)

        unique_products.append(product)

        print(f"Unique products: "
              f"{len(unique_products)}")
        
    # scarping product pages 
    final_products = []
    total = len(unique_products)
    
    for index, product in enumerate(
        unique_products,
        start=1
    ):

        print(
            f"\n[{index}] Processing..."
        )

        try:

            details = scrape_product_page(
                driver,
                product["product_url"]
            )

            merged = {
                **product,
                **details
            }

            # Clean URL 
            merged["product_url"]=( f"https://www.amazon.in/dp/"
                f"{merged['asin']}")
            
            # removing duplicate fields
            merged.pop("title",None)
            merged.pop("image_url",None)
            final_products.append(merged)

        except Exception as e:
            print(f"Error scraping "
                f"{product['asin']}")
            print(e)

    # close browser AFTER all products
    driver.quit()

    # create dataframe AFTER loop
    df = pd.DataFrame(
        final_products
    )

    os.makedirs("output", exist_ok=True)

    csv_file = os.path.join(
    "output",
    f"{category}.csv")
    
    df.to_csv(
        csv_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"\nCSV saved: {csv_file}"
    )

    print(f"Total Rows: "
          f"{len(df)}")

if __name__ == "__main__":
    main()