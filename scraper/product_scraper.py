from bs4  import BeautifulSoup
import time

def scrape_product_page(driver, product_url):

    driver.get(product_url)

    # page loading time 
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "lxml")
    product_data = {}

    # product title
    title_tag = soup.find(id = "productTitle")
    if title_tag:

        product_data["full_title"]= (title_tag.get_text(strip = True))

    # product iamge
    image_tag = soup.find(id = "landingImage")
    if image_tag:

        product_data["product_image"]=(image_tag.get("src"))

    # product price 

    price_tag = soup.select_one("span.a-price span.a-offscreen")

    if price_tag :
        product_data["product_price"]= (
            price_tag.get_text(strip = True)
        )
    # product specifications 

    spec_table = soup.select_one( "table.a-normal.a-spacing-micro")

    if spec_table:

        rows = spec_table.find_all("tr")

        for row in rows:
            key_tag = row.find("span", class_= "a-text-bold")
            value_tag = row.find("span", class_="po-break-word")

            if key_tag and value_tag:

                key = key_tag.get_text(strip = True)
                value = value_tag.get_text(strip = True)

                #  converting keys to CSV-friendly format

                key = (
                    key.lower().replace(" ","_").replace("/","_")
                )
                product_data[key] = value
    return product_data

    