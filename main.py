from scraper.selenium_driver import get_driver
from scraper.search_scraper import (
    scrape_search_page,
    get_total_pages
)
from scraper.product_scraper import scrape_product_page
from datetime import datetime

import pandas as pd
import os
import time
import random 

def human_delay(min_time=2, max_time=5):
    # this will return a random decimal between 2 and  5
    delay = random.uniform(min_time, max_time)
    print(f"Waiting for "
          f"{delay: .2f} second....")
    time.sleep(delay)



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

    # data structures for storing the products

    # stores all the successfully scraped products
    final_products = []

    # used to remove duplicate products
    seen_asins = set()

    # stores the products that failed after all the retries 
    failed_products = []

    # this is used to store the ASIN'S that are already prsent in the CSV 
    scraped_asins = set()

    # Check if the csv already exists 
    if os.path.exists(csv_file):
        print("\n Existing CSV found")
        old_df = pd.read_csv(csv_file)

        # Load previously scraped products 
        final_products = old_df.to_dict(orient="records")

        #Store all the previously scrapped ASINS
        scraped_asins = set(old_df["asin"].astype(str))

        print(f"Found"
              f"{len(scraped_asins)}"
              f"already scraped products.")


    # configurations
    SAVE_INTERVAL = 10
    MAX_RETRIES = 2
    RETRY_DELAY = 3

  


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

                # skip the products already present in CSV 
                if asin in scraped_asins:
                    print(f"Already Scraped : "
                        f"{asin}")
                    continue
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
                last_error = ""

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

                        # temp for  testing 
                        #if asin == "B09MM58Y7Q":
                           # raise Exception("Testing Failed Product Logging")

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
                        seen_asins.add(asin)

                        success = True

                        print(
                            f"Scraped Successfully "
                            f"({len(final_products)})"
                        )

                        human_delay()

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
                        
                        last_error = str(e)
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

                            human_delay(
                                RETRY_DELAY,RETRY_DELAY + 3)

                # product failed after all retries
                if not success:

                    print(
                        f"Skipping Product : "
                        f"{asin}"
                    )

                    failed_products.append({
                        "asin" : asin,
                        "product_url" : product["product_url"],
                        "category" : category,
                        "attempts" : MAX_RETRIES+1,
                        "error" : last_error ,
                        "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    })
                    print("\nAdded to failed products list")
                    print(failed_products[-1])

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

        # create log folder if it dosen't exist 
        os.makedirs("logs", exist_ok = True)
        failed_log_file = os.path.join("logs",f"{category}_failedproducts.csv")

        # Save successful products 
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
        
        #Save failed products 
        if failed_products:

            failed_df = pd.DataFrame(failed_products)
            failed_df.to_csv(failed_log_file, index = False, encoding = "utf-8-sig")
            print(f"\n Failed Products Log Saved : "
                  f"{failed_log_file}")
            print(f"Failed Products : "
                  f"{len(failed_df)}")
            
        print("\n==============================")

        print(
            f"Successful Products : "
            f"{len(final_products)}"
        )

        print(
            f"Failed Products : "
            f"{len(failed_products)}"
        )

        print("==============================")
    

   

if __name__ == "__main__":
    main()

    


