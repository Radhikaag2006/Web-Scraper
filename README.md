# Amazon Product Scraper

## Overview

Amazon Product Scraper is a Python-based web scraping application that extracts product information from Amazon search results and individual product pages using Selenium and BeautifulSoup.

The scraper collects product listings for a user-provided category, visits each product page, extracts detailed specifications, and exports the collected data into a structured CSV file.

The project is designed with a modular architecture, making it easy to extend, maintain, and customize for different product categories.

---

## Features

* Search products by category.
* Automatically scrape multiple search result pages.
* Skip sponsored products.
* Extract product information from search results.
* Visit individual product pages for detailed specifications.
* Export data to CSV format.
* Modular project structure for easy maintenance.
* Supports multiple product categories.

---

## Data Extracted

For every product, the scraper collects:

* ASIN
* Product Title
* Sale Price
* MRP
* Product URL
* Product Image URL
* Product Image
* Product Price
* Brand
* Model Name
* Screen Size
* Colour
* Hard Disk Size
* CPU Model
* RAM Memory Installed Size
* Operating System
* Special Features
* Graphics Card Description

The available specifications may vary depending on the product category and the information provided by Amazon.

---

## Project Structure

```
AmazonScraper/
│
├── config/
│   └── settings.py
│
├── scraper/
│   ├── selenium_driver.py
│   ├── search_scraper.py
│   └── product_scraper.py
│
├── utils/
│   ├── csv_handler.py
│   └── helpers.py
│
├── tests/
│
├── output/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies Used

* Python 3
* Selenium
* BeautifulSoup4
* Pandas
* Requests
* lxml

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/AmazonScraper.git
```

Navigate to the project directory:

```bash
cd AmazonScraper
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application:

```bash
python main.py
```

Enter a product category when prompted:

```
Enter category:
laptop
```

The scraper will:

1. Search Amazon for the specified category.
2. Collect product URLs from search results.
3. Visit each product page.
4. Extract detailed product information.
5. Save the results as a CSV file inside the `output` directory.

---

## Example Output

```
output/
└── laptop.csv
```

Sample columns:

```
asin
full_title
product_price
sale_price
mrp
brand
model_name
screen_size
ram_memory_installed_size
operating_system
graphics_card_description
product_url
product_image
```

---

## Design Workflow

```
User Input
      │
      ▼
Search Amazon
      │
      ▼
Extract Product URLs
      │
      ▼
Visit Product Pages
      │
      ▼
Extract Specifications
      │
      ▼
Merge Product Data
      │
      ▼
Export CSV
```

---

## Notes

* Selenium is used to render JavaScript-generated content.
* BeautifulSoup is used to parse HTML and extract data.
* Product specifications may differ across categories.
* Sponsored products are skipped during scraping.
* The scraper stores the generated CSV files inside the `output` directory.

---

## Future Improvements

* Automatically detect the total number of available search result pages.
* Implement explicit Selenium waits instead of fixed delays.
* Add logging for better debugging.
* Support parallel scraping for improved performance.
* Add retry mechanisms for temporary request failures.
* Support exporting data in JSON and Excel formats.

---

## Disclaimer

This project is intended for educational and learning purposes only. Users should ensure that they comply with Amazon's Terms of Service and applicable laws when scraping publicly available web content.
