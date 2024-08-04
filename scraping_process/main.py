import multiprocessing
from pages_ads import fetch_and_parse_ad_links
from property_features import RealEstateProperty
import json
import logging
from functools import partial

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_provinces = ['hainaut', 'namur', 'walloon-brabant', 'liege', 'luxembourg', 'west-flanders', 'east-flanders', 'antwerp', 'flemish-brabant', 'limburg', 'brussels']

def process_ad_url(province, ad_url):
    """
    Processes a single ad URL by scraping its property details and saving them to a JSON file.

    Args:
        province (str): The province of the property.
        ad_url (str): The URL of the property ad.
    """
    try:
        property = RealEstateProperty(ad_url)
        property.page_scraper()
        property.save_to_json(province)
    except Exception as e:
        logging.error(f"Error processing {ad_url}: {e}")

def main():
    """
    Main function to fetch ad links, scrape property details, and save them to JSON files.

    For each province in `list_provinces`, this function:
    1. Fetches a list of ad URLs.
    2. Uses multiprocessing to process each ad URL in parallel.
    3. Scrapes property details from each ad page.
    4. Saves the scraped data to individual JSON files for each province.
    5. Aggregates all province data into a single JSON file.
    """
    list_of_all_province_data = []

    for province in list_provinces:
        try:
            # Fetch list of ad URLs for the province
            list_of_ads = fetch_and_parse_ad_links(province)
            num_processes = multiprocessing.cpu_count()
            logging.info(f"Starting multiprocessing with {num_processes} processes for province: {province}")
            
            # Create a new function with 'province' as a fixed argument
            # This allows process_ad_url to be called with only 'ad_url' during multiprocessing
            partial_process_ad_url = partial(process_ad_url, province)
            
            # Use multiprocessing pool to process ad URLs in parallel
            with multiprocessing.Pool(processes=num_processes) as pool:
                pool.map(partial_process_ad_url, list_of_ads)
            
            logging.info(f"Multiprocessing complete for province: {province}")
            
            # Read the saved JSON file for the current province and append the data to the list
            with open(f"properties_{province}_rent.json", 'r') as f:
                data = json.load(f)
                list_of_all_province_data.append(data)
        
        except Exception as e:
            logging.error(f"Error processing province {province}: {e}")
    
    # Save all province data into a single JSON file
    with open('all_json_files_content_rent.json', 'w') as f:
        json.dump(list_of_all_province_data, f, indent=4)

if __name__ == "__main__":
    main()