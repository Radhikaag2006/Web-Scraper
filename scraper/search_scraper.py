from bs4 import BeautifulSoup
import time


def get_total_pages(driver, category):
    """
    Returns the total number of pages
    available for the given category.
    """

    url = (
        f"https://www.amazon.in/s?"
        f"k={category}&page=1"
    )

    driver.get(url)

    # Wait for page to load
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "lxml")

    # Find pagination container
    pagination = soup.select_one(".s-pagination-container")

    # If pagination doesn't exist,
    # there is only one page
    if pagination is None:
        return 1

    page_numbers = []

    # Get all pagination items
    items = pagination.select(".s-pagination-item")

    for item in items:

        text = item.get_text(strip=True)

        # Keep only numbers
        if text.isdigit():
            page_numbers.append(int(text))

    # If no numbers found
    if not page_numbers:
        return 1

    total_pages = max(page_numbers)

    print(f"\nTotal Pages Found: {total_pages}")

    return total_pages

def scrape_search_page(driver, category, page=1):

    url = (
        f"https://www.amazon.in/s?"
        f"k={category}&page={page}"
    )

    driver.get(url)

    time.sleep(3)

    soup = BeautifulSoup(
        driver.page_source,
        "lxml"
    )

    product_cards = soup.select(
        'div[data-component-type="s-search-result"]'
    )

    print(
        f"Found {len(product_cards)} cards"
    )

    products = []

    sponsored_skipped = 0

    for card in product_cards:

        asin = card.get(
            "data-asin",
            ""
        ).strip()

        if not asin:
            continue

        title = None
        image_url = None
        product_url = None
        sale_price = None
        mrp = None

        # TITLE

        h2 = card.find("h2")

        if h2:
            title = h2.get_text(
                strip=True
            )

        # PRODUCT LINK
    
        a_tag = card.find(
            "a",
            href=True
        )

        if a_tag:

            href = a_tag["href"]

            # skip sponsored products

            if "/sspa/" in href:

                sponsored_skipped += 1
                continue

            if href.startswith("/"):

                product_url = (
                    "https://www.amazon.in"
                    + href
                )

            else:

                product_url = href

        # IMAGE URL

        img = card.find("img")

        if img:

            image_url = img.get("src")

        # SALE PRICE
        
        sale_price_tag = card.select_one(
            'span.a-price:not(.a-text-price) span.a-offscreen'
        )

        if sale_price_tag:

            sale_price = (
                sale_price_tag.get_text(
                    strip=True
                )
            )

        # MRP
        
        mrp_tag = card.select_one(
            'span.a-price.a-text-price span.a-offscreen'
        )

        if mrp_tag:

            mrp = (
                mrp_tag.get_text(
                    strip=True
                )
            )

        products.append(
            {
                "asin": asin,
                "title": title,
                "sale_price": sale_price,
                "mrp": mrp,
                "image_url": image_url,
                "product_url": product_url
            }
        )

    print(
        f"Sponsored products skipped: "
        f"{sponsored_skipped}"
    )

    return products
