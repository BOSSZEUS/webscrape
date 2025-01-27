from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Initialize the web driver (Make sure you have the correct driver for your browser)
driver = webdriver.Chrome()  # Update the path if necessary

# Open Madeira USA website
driver.get("https://www.madeirausa.com/")

# Function to search for thread number and extract the color information
def search_thread(thread_number):
    try:
        # Wait for the search bar to load and interact with it
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#Keywords"))
        )
        search_bar.clear()
        search_bar.send_keys(thread_number)
        search_bar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder_PageContent1_FilterProductResults_Repeater_SearchResultsGrid_ctl01_Result > div > div.shortDesc")
            )
        )
        time.sleep(2)  # Ensure all elements load completely

        # Extract the search results
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = []

        # Use the provided selector to extract thread descriptions
        for item in soup.select("#ctl00_ContentPlaceHolder_PageContent1_FilterProductResults_Repeater_SearchResultsGrid_ctl01_Result > div > div.shortDesc"):
            results.append(item.text.strip())

        return results

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

# Define the thread numbers to search for
thread_numbers = ["1234", "5678", "91011"]  # Replace with actual thread numbers
results = {}

# Perform the search for each thread number
for thread in thread_numbers:
    print(f"Searching for thread number: {thread}")
    results[thread] = search_thread(thread)

# Close the driver
driver.quit()

# Display the results
for thread, data in results.items():
    print(f"Results for thread number {thread}:")
    for entry in data:
        print(f"  - {entry}")
