from scraper.selenium_driver import get_driver
from scraper.search_scraper import (
    scrape_search_page,
    get_total_pages
)
from scraper.product_scraper import scrape_product_page

import pandas as pd
import os


def main():

    category = input(
        "Enter category: "
    ).strip()

    driver = get_driver()

    # ==============================
    # Detect total pages
    # ==============================

    total_pages = get_total_pages(
        driver,
        category
    )


    all_search_products = []

    # ==============================
    # Scrape all search pages
    # ==============================

    for page in range(1, total_pages + 1):

        print(
            f"\nScraping Search Page {page}/{total_pages}"
        )

        products = scrape_search_page(
            driver,
            category,
            page=page
        )

        all_search_products.extend(products)

    print(
        f"\nTotal Products Found: "
        f"{len(all_search_products)}"
    )

    # ==============================
    # Remove duplicate ASINs
    # ==============================

    seen_asins = set()
    unique_products = []

    for product in all_search_products:

        asin = product["asin"]

        if asin in seen_asins:
            continue

        seen_asins.add(asin)
        unique_products.append(product)

    print(
        f"\nUnique Products: "
        f"{len(unique_products)}"
    )

    # ==============================
    # Scrape product pages
    # ==============================

    final_products = []

    total = len(unique_products)

    for index, product in enumerate(
        unique_products,
        start=1
    ):

        print(
            f"\n[{index}/{total}] "
            f"Scraping {product['asin']}"
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

            # Clean Product URL
            merged["product_url"] = (
                f"https://www.amazon.in/dp/"
                f"{merged['asin']}"
            )

            # Remove duplicate fields
            merged.pop("title", None)
            merged.pop("image_url", None)

            final_products.append(
                merged
            )

        except Exception as e:

            print(
                f"Error scraping "
                f"{product['asin']}"
            )

            print(e)

    # ==============================
    # Close browser
    # ==============================

    driver.quit()

    # ==============================
    # Save CSV
    # ==============================

    df = pd.DataFrame(
        final_products
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    csv_file = os.path.join(
        "output",
        f"{category}.csv"
    )

    df.to_csv(
        csv_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"\nCSV saved: {csv_file}"
    )

    print(
        f"Total Rows: {len(df)}"
    )


if __name__ == "__main__":
    main()
