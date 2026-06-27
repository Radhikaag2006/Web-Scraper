from scraper.selenium_driver import get_driver
from scraper.search_scraper import (
    scrape_search_page,
    get_total_pages
)
from scraper.product_scraper import scrape_product_page

import pandas as pd
import os
import time


def main():

    category = input(
        "Enter category: "
    ).strip()

    driver = get_driver()

    os.makedirs(
        "output",
        exist_ok=True
    )

    csv_file = os.path.join(
        "output",
        f"{category}.csv"
    )

    SAVE_INTERVAL = 10
    MAX_RETRIES = 2
    RETRY_DELAY = 3

    final_products = []

    try:

        # Detect Total Pages

        total_pages = get_total_pages(
            driver,
            category
        )

        # Uncomment while testing
        # total_pages = min(total_pages, 2)

        all_search_products = []

        # Scrape Search Pages

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

        # Remove Duplicate Products

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

        # Scrape Product Pages

        total = len(unique_products)

        for index, product in enumerate(
            unique_products,
            start=1
        ):

            print(
                f"\n[{index}/{total}] "
                f"Scraping {product['asin']}"
            )

            success = False

            for attempt in range(1, MAX_RETRIES + 2):

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

                    success = True

                    # Auto-save
                    if len(final_products) % SAVE_INTERVAL == 0:

                        df = pd.DataFrame(
                            final_products
                        )

                        df.to_csv(
                            csv_file,
                            index=False,
                            encoding="utf-8-sig"
                        )

                        print(
                            f"\nAuto-saved "
                            f"{len(final_products)} products."
                        )

                    break

                except Exception as e:

                    print(
                        f"\nAttempt {attempt} failed "
                        f"for {product['asin']}"
                    )

                    print(e)

                    if attempt <= MAX_RETRIES:

                        print(
                            f"Retrying in "
                            f"{RETRY_DELAY} seconds..."
                        )

                        time.sleep(RETRY_DELAY)

            if not success:

                print(
                    f"Skipping "
                    f"{product['asin']}"
                )

    except KeyboardInterrupt:

        print(
            "\n\nScraping interrupted by user."
        )

    finally:

        print(
            "\nSaving scraped data..."
        )

        driver.quit()

        if final_products:

            df = pd.DataFrame(
                final_products
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
                f"Total Rows: "
                f"{len(df)}"
            )

        else:

            print(
                "\nNo products were scraped."
            )


if __name__ == "__main__":
    main()