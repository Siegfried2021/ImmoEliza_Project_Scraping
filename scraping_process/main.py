import multiprocessing
from pages_ads import fetch_and_parse_ad_links
from property_features import RealEstateProperty
import json
import logging
from functools import partial

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_provinces = ['hainaut', 'namur', 'walloon-brabant', 'liege', 'luxembourg', 'west-flanders', 'east-flanders', 'antwerp', 'flemish-brabant', 'limburg', 'brussels']

def process_ad_url(province, ad_url):
    try:
        property = RealEstateProperty(ad_url)
        property.page_scraper()
        property.save_to_json(province)
        # logging.info(f"Processed property {property.id}")

    except Exception as e:
        logging.error(f"Error processing {ad_url}: {e}")

def main():
    list_of_all_province_data = []
    
    for province in list_provinces:
        try:
            list_of_ads = fetch_and_parse_ad_links(province)
            # logging.info(f"Total ad URLs fetched: {len(list_of_ads)}")

            num_processes = multiprocessing.cpu_count() 
            logging.info(f"Starting multiprocessing with {num_processes} processes")
            
            partial_process_ad_url = partial(process_ad_url, province)
            
            with multiprocessing.Pool(processes=num_processes) as pool:
                pool.map(partial_process_ad_url, list_of_ads)
            
            logging.info("Multiprocessing complete.")
            
            with open(f"properties_{province}_rent.json", 'r') as f:
                data = json.load(f)
                list_of_all_province_data.append(data)
        
        except Exception as e:
            logging.error(f"Main process error: {e}")
    
    with open('all_json_files_content_rent.json', 'w') as f:
        json.dump(list_of_all_province_data, f, indent=4)

if __name__ == "__main__":
    main()