import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import random

# --- Setup ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
base_link = 'https://eg.hatla2ee.com'
all_car_details = []

# Define the exact start and end pages for this script
START_PAGE = 1
END_PAGE = 2

for i in tqdm(range(START_PAGE, END_PAGE + 1), desc=f"Scraping Pages {START_PAGE}-{END_PAGE}"):
    url = f'https://eg.hatla2ee.com/en/car/page/{i}'
    try:
        page_response = requests.get(url, headers=HEADERS, timeout=20)
        page_response.raise_for_status() 
        #If the request failed a 403 Forbidden error because you're blocked, this line will stop the script immediately and raise an HTTPError.
        page = page_response.text
        soup = BeautifulSoup(page, 'html.parser')
        
        
        car_containers = soup.find_all('div', class_='newCarListUnit_wrap')

        if not car_containers:
            print(f"\nNo car listings found on page {i}. This might be the last page or the class name changed again.")
            break

        for car in car_containers:
            try:
                header_div = car.find('div', class_='newCarListUnit_header')
                if not header_div or not header_div.find('a'):
                    continue
                
                link_tag = header_div.find('a')
                link_url = link_tag.get('href')
                full_url = base_link + link_url
                
                # Retry mechanism for getting the detail page
                sub_page = None
                for attempt in range(3):
                    try:
                        sub_page_response = requests.get(full_url, headers=HEADERS, timeout=20)
                        sub_page_response.raise_for_status()
                        sub_page = sub_page_response.text
                        break
                    except requests.exceptions.RequestException as e:
                        print(f"\nAttempt {attempt + 1} failed for {full_url}. Error: {e}. Retrying...")
                        time.sleep(attempt * 2 + 1)
                
                if sub_page is None:
                    print(f"\nCould not retrieve {full_url} after multiple attempts. Skipping.")
                    continue

                detail_soup = BeautifulSoup(sub_page, "html.parser")
                
                current_car_details = {'URL': full_url}
                price_span = detail_soup.find('span', class_='usedUnitCarPrice')
                current_car_details['Price'] = price_span.text.strip() if price_span else "N/A"

                date_tag = detail_soup.find('div', class_='galleryIconWrap date')
                current_car_details['Date'] = date_tag.find('span').text.strip() if date_tag else "N/A"
                
                desc_items = detail_soup.find_all('div', class_='DescDataItem')
                for item in desc_items:
                    label_tag = item.find('span', class_='DescDataSubTit')
                    value_tag = item.find('span', class_='DescDataVal')
                    if label_tag and value_tag:
                        label = label_tag.text.strip()
                        value = value_tag.text.strip()
                        current_car_details[label] = value
                
                all_car_details.append(current_car_details)
                # Random time to wait to act like a humnan so the request appear less robotic
                time.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"\nCould not process one car. Error: {e}. Skipping.")

    except Exception as e:
        print(f"\nCould not load page {i}. Error: {e}")

# --- Final saving step ---
print(f"\nScraping complete. Successfully scraped details for {len(all_car_details)} cars.")

if all_car_details:
    df = pd.DataFrame(all_car_details)
    if 'The model' in df.columns:
        df = df.rename(columns={'The model': 'Model'})

    output_file = f'hatla2ee_scraped_cars_{START_PAGE}-{END_PAGE}.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"All data saved to '{output_file}'")