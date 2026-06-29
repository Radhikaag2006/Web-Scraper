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

    # taking input from user
    category = input(
        "Enter category: "
    ).strip()

    # creating selenium driver
    driver = get_driver()

    # creating output folder
    os.makedirs(
        "output",
        exist_ok=True
    )

    csv_file = os.path.join(
        "output",
        f"{category}.csv"
    )

    # configurations
    SAVE_INTERVAL = 10
    MAX_RETRIES = 2
    RETRY_DELAY = 3

    # data structures for storing the products

    # stores all the successfully scraped products
    final_products = []

    # used to remove duplicate products
    seen_asins = set()

    try:

        # finding total number of search pages from html
        total_pages = get_total_pages(
            driver,
            category
        )

        print(
            f"\nTotal Pages Found : "
            f"{total_pages}"
        )

        # testing
        total_pages = min(
            total_pages,
            2
        )

        # looping through every search page
        for page in range(
            1,
            total_pages + 1
        ):

            print(
                f"\nScraping Search Page "
                f"{page}/{total_pages}"
            )

            print()

            # extracting products from ONE search page
            products = scrape_search_page(
                driver,
                category,
                page
            )

            print(
                f"Products Found : "
                f"{len(products)}"
            )

            # processing every product immediately
            for product in products:

                asin = product["asin"]

                # skip duplicate ASIN's
                if asin in seen_asins:
                    continue

                # otherwise add them to set
                seen_asins.add(
                    asin
                )

                print(
                    f"\nScraping Product : "
                    f"{asin}"
                )

                success = False

                # retry mechanism
                for attempt in range(
                    1,
                    MAX_RETRIES + 2
                ):

                    try:

                        details = scrape_product_page(
                            driver,
                            product["product_url"]
                        )

                        # merge search page data with product page
                        merged = {
                            **product,
                            **details
                        }

                        # save clean URL'S
                        merged["product_url"] = (
                            f"https://www.amazon.in/dp/{asin}"
                        )

                        # remove duplicate columns
                        merged.pop(
                            "title",
                            None
                        )

                        merged.pop(
                            "image_url",
                            None
                        )

                        final_products.append(
                            merged
                        )

                        success = True

                        print(
                            f"Scraped Successfully "
                            f"({len(final_products)})"
                        )

                        # auto saving the products
                        if (
                            len(final_products)
                            % SAVE_INTERVAL
                            == 0
                        ):

                            df = pd.DataFrame(
                                final_products
                            )

                            df.to_csv(
                                csv_file,
                                index=False,
                                encoding="utf-8-sig"
                            )

                            print(
                                f"\nAuto Saved "
                                f"{len(final_products)} "
                                f"Products"
                            )

                        # stop retrying after success
                        break

                    except Exception as e:

                        print(
                            f"\nAttempt "
                            f"{attempt} Failed"
                        )

                        print(e)

                        if attempt <= MAX_RETRIES:

                            print(
                                f"Retrying after "
                                f"{RETRY_DELAY} "
                                f"seconds..."
                            )

                            time.sleep(
                                RETRY_DELAY
                            )

                # product failed after all retries
                if not success:

                    print(
                        f"Skipping Product : "
                        f"{asin}"
                    )

    # user interrupts the scraper
    except KeyboardInterrupt:

        print(
            "\n\nScraping Interrupted "
            "by User."
        )

    # always executes
    finally:

        print(
            "\nSaving Final CSV...."
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
                f"\nCSV Saved : "
                f"{csv_file}"
            )

            print(
                f"Total Products : "
                f"{len(df)}"
            )

        else:

            print(
                "\nNo Products Were Scraped."
            )


if __name__ == "__main__":
    main()

    


