from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Initialize the web driver (Ensure you have the correct driver for your browser)
driver = webdriver.Chrome()  # You may need to specify the path to your ChromeDriver

# Open Madeira USA website
driver.get("https://www.madeirausa.com/")

# Define a function to search for a thread number and extract its color
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
            EC.presence_of_element_located((By.CSS_SELECTOR, ".shortDesc"))
        )
        time.sleep(2)  # Additional wait to ensure all elements load

        # Extract the search result page's content
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Filter results for 5500y length
        results = []
        for item in soup.select(".shortDesc"):
            parent_div = item.find_parent("div")
            if "5500y" in parent_div.text.lower():
                results.append({
                    "description": item.text.strip(),
                    "details": parent_div.text.strip(),
                })

        return results

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

# Input the thread numbers you want to search for
thread_numbers = ['1000', '1001', '1002', '1005', '1006', '1010', '1011', '1012', '1013', '1021', '1023', '1024', '1025', '1028', '1029', '1030', '1032']  # Replace with actual thread numbers
results = {}

# Loop through each thread number and collect results
for thread in thread_numbers:
    print(f"Searching for thread number: {thread}")
    results[thread] = search_thread(thread)

# Close the driver
driver.quit()

# Print the results
for thread, data in results.items():
    print(f"Results for thread number {thread}:")
    for entry in data:
        print(f"  - {entry['description']}: {entry['details']}")
