from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 

def get_driver():
  options = Options()

  while True:
    mode = input("Would you like to run it in headless mode? (y/n):").strip().lower()
    if mode in ("y", "n"):
      break
    print("Please enter only 'y' or 'n'.")

  headless = mode == "y"

  if headless:
    options.add_argument("--headless=new")

  options.add_argument("--start-maximized")
  driver = webdriver.Chrome(options=options)
  return driver
