from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# Class names are always changing please check classes' names on the website (ContactCars.com)


# Humnan scraping function 
def human_scroll_to_bottom(driver, pause_time=1.5):
    """
    Scrolls to the bottom of the page in a human-like way,
    waiting for new content to load.
    """
    # Get the initial height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait a random amount of time for the page to load
        time.sleep(random.uniform(pause_time - 0.5, pause_time + 0.5))
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            # If the heights are the same, we've reached the bottom
            print("Reached the bottom of the page.")
            break
        
        # Update the height for the next loop
        last_height = new_height

# --- Selenium Setup ---
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')# We are still in VISIBLE mode for this test
# goal is to make your Selenium browser look as human as possible and prevent it from crashing.
# Start the driver
# Note: undetected_chromedriver downloads and patches the driver automatically
print("Starting Undetected Chrome... Please wait.")



base_link = 'https://www.contactcars.com'

try:
    driver = uc.Chrome(options=options)
    print("Driver started. Do not minimize the window.")
except Exception as e:
    print(f"Error starting Selenium: {e}")
    exit()

print("Selenium driver started in VISIBLE mode.")
print("!!! DO NOT use the Chrome window while the script is running. !!!")

all_car_details = []
START_PAGE = 1
END_PAGE = 2  

for i in tqdm(range(START_PAGE, END_PAGE + 1), desc=f"Scraping Pages {START_PAGE}-{END_PAGE}"):
    url = f'https://www.contactcars.com/en/used-cars?page={i}'
    try:
        driver.get(url)
        print(f"\nPage {i}: Scrolling down to load cars...")
        for _ in range(3): # Scroll down 3 times
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            # Wait for content to load after each scroll
            time.sleep(random.uniform(1.5, 2.5))
        # We use By.CSS_SELECTOR to handle the multiple classes
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.flex.flex-wrap.mt-4"))
            )
        except Exception as e:
            print(f"\nPage {i} timed out waiting for car list (ul container).")
            driver.save_screenshot(f'screenshot_page_{i}.png')
            print(f"Saved screenshot_page_{i}.png for debugging.")
            continue 

        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        
        # This logic is now safe because we waited for the 'ul'
        cars_block = soup.find('ul', class_='flex flex-wrap mt-4')
        if not cars_block:
            print(f"\nCould not find 'ul' container on page {i} even after waiting.")
            continue 

        car_containers = cars_block.find_all('li')
        if not car_containers:
            print(f"\nFound 'ul' but no 'li' car listings on page {i}.")
            continue

        for car in car_containers:
            try:
                link_tag = car.find('a', class_='block relative h-60 w-full')
                if not link_tag or not link_tag.get('href'):
                    continue
                
                link_url = link_tag.get('href') 
                full_url = base_link + link_url
                
                driver.get(full_url)
                
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='#price']")) 
                    )
                except Exception as e:
                    print(f"\nDetail page {full_url} timed out. Skipping car.")
                    continue
                    
                detail_page_html = driver.page_source
                detail_soup = BeautifulSoup(detail_page_html, "html.parser")
                
                current_car_details = {'URL': full_url}

                # Your scraping logic (which was correct)
                price_div = detail_soup.find('div', id='#price') 
                current_car_details['Price'] = price_div.find('h3').text.strip() if price_div else "N/A"
                
                city_div = detail_soup.find('div' , class_='h-[22px] flex items-center gap-2 text-brand-900 txt-md')
                cc = city_div.find_all('span')
                current_car_details['City'] = City = cc[0].text.strip()
                current_car_details['Country'] = Country = cc[1].text.strip()
                

                date_tag = detail_soup.find('span', class_='txt-md text-brand-900 text-start')
                current_car_details['Date'] = date_tag.text.strip() if date_tag else "N/A"

                title_div = detail_soup.find('div',class_='order-2 md:order-1')
                if title_div:
                    title_spans = title_div.find_all('span', class_='inline-block')
                    if title_spans:
                        title_parts = [span.text.strip() for span in title_spans]
                        current_car_details['Title'] = " ".join(title_parts)
                        current_car_details['Make'] = title_parts[0] if len(title_parts) > 0 else "N/A"
                        current_car_details['Model'] = title_parts[1] if len(title_parts) > 1 else "N/A"
                        current_car_details['Year'] = title_parts[-1] if len(title_parts) > 2 else "N/A"
                        
                desc_block = detail_soup.select_one("div.grid.grid-cols-2.gap-3")

                if desc_block:
                    desc_items = desc_block.select("div.flex.flex-col")
                    
                    for item in desc_items:
                        label_tag = item.select_one("span.text-dark-blue")
                        value_tag = item.select_one("h5")

                        if label_tag and value_tag:
                            key = label_tag.text.strip()
                            value = value_tag.text.strip()
                            
                            current_car_details[key] = value

                else:
                    print("Could not find the main description block.")
                
                all_car_details.append(current_car_details)
                time.sleep(random.uniform(5, 15))
                
            except Exception as e:
                print(f"\nCould not process one car. Error: {e}. Skipping.")

    except Exception as e:
        print(f"\nCould not load page {i}. Error: {e}")

driver.quit()

# --- Save to Excel ---
print(f"\nScraping complete. Successfully scraped details for {len(all_car_details)} cars.")

if all_car_details:
    df = pd.DataFrame(all_car_details)
    print("--- Sample of Scraped Data ---")
    print(df.head())
    
    df.to_excel(f"contactcars_scraped_data{START_PAGE}-{END_PAGE}.xlsx", index=False, engine='openpyxl')
    print("\nData saved to 'contactcars_scraped_data{START_PAGE}-{END_PAGE}.xlsx'")
else:
    print("No data was scraped.")