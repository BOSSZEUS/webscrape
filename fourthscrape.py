import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the web driver (Ensure you have the correct driver for your browser)
driver = webdriver.Chrome()  # Update the path to ChromeDriver if necessary

# Open Madeira USA website
driver.get("https://www.madeirausa.com/")

# Define a function to search for a thread number, filter results, and extract the simplified paragraph or color
def search_thread(thread_number):
    try:
        print(f"Searching for thread number: {thread_number}")

        # Wait for the search bar to load and interact with it
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#Keywords"))
        )
        search_bar.clear()
        search_bar.send_keys(thread_number)
        search_bar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder_PageContent1_FilterProductResults_Repeater_SearchResultsGrid_ctl01_pnlAddToCart > a"))
        )
        time.sleep(2)  # Additional wait to ensure all elements load

        # Locate the link for adding to cart (as the click target)
        add_to_cart_link = driver.find_element(
            By.CSS_SELECTOR,
            "#ctl00_ContentPlaceHolder_PageContent1_FilterProductResults_Repeater_SearchResultsGrid_ctl01_pnlAddToCart > a"
        )

        # Click the link to navigate to the second page
        add_to_cart_link.click()

        # Wait for the detail page to load
        paragraph_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                # for Rayon threads
                # (By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder_PageContent1_ProductDetail_pnlSingleItemDetail > div.desc > p:nth-child(7)")
                # for Polyneon Threads
                (By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder_PageContent1_ProductDetail_pnlSingleItemDetail > div.desc > p")
            )
        )

        # Extract the paragraph text
        paragraph_text = paragraph_element.text.strip()

        # Use improved regex to extract the relevant color and simplified text
        match = re.search(
            r"#\d+-\d+\s.*?(?:in|of)\s(.+?)(?:\.|$)",  # Captures the color after "in" or "of"
            paragraph_text,
            re.IGNORECASE,
        )
        if match:
            simplified_paragraph = match.group(0).strip()
            color = match.group(1).strip()
        else:
            simplified_paragraph = paragraph_text
            color = "N/A"

        print(f"Found paragraph: {simplified_paragraph}")
        print(f"Found color: {color}")
        return {"thread_number": thread_number, "paragraph": simplified_paragraph, "color": color}

    except Exception as e:
        print(f"Error occurred for thread {thread_number}: {e}")
        return None
    finally:
        # Navigate back to the main page for the next search
        driver.get("https://www.madeirausa.com/")

# Input the thread numbers you want to search for
thread_numbers =  [1905, 1906, 1907, 1908, 1909, 1910, 1911, 1915, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]

results = {}

# Loop through each thread number and collect results
for thread in thread_numbers:
    print(f"Processing thread number: {thread}")
    results[thread] = search_thread(thread)

# Close the driver
driver.quit()

# Print the results
for thread, data in results.items():
    if data:
        print(f"Thread {thread}: Paragraph - {data['paragraph']}, Color - {data['color']}")
    else:
        print(f"Thread {thread}: No data found")
