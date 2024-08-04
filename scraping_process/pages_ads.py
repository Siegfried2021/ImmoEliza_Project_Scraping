import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import multiprocessing
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_page(url):
    try:
        headers = {"User-agent":"mathieu", "Authorization":"mathieu2"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
 
        if response.status_code == 200:
            html = response.text
            # logging.debug(f"Fetched page from {url}")
            return html

        else:
            logging.warning(f"Page {url} does not exist. Status code: {response.status_code}")
            return None
        
    except RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
        return None

def parse_page_for_ads(html):
    soup = BeautifulSoup(html, 'html.parser')
    h2_elements = soup.find_all('h2')
    list_ad_urls = []
    for h2 in h2_elements:
        a_element = h2.find('a', class_='card__title-link')
        if a_element and 'href' in a_element.attrs:
            ad_url = a_element['href']
            list_ad_urls.append(ad_url)
    # logging.debug(f"Parsed {len(list_ad_urls)} ad URLs from page")
    return list_ad_urls

def fetch_and_parse_page(url):
    html = fetch_page(url)
    if html:
        page_ad_urls = parse_page_for_ads(html)
        return page_ad_urls
    else:
        return []

def fetch_and_parse_ad_links(province):
    # root_url_for_sale = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale'
    root_url_for_rent = 'https://www.immoweb.be/en/search/house-and-apartment/for-rent'
    # list_of_page_urls_for_sale = [f"{root_url_for_sale}/{province}/province?countries=BE&isALifeAnnuitySale=false&isAPublicSale=false&page={i}&orderBy=relevance" for i in range(1, 301)]
    list_of_page_urls_for_rent = [f"{root_url_for_rent}/{province}/province?countries=BE&page={i}&orderBy=relevance" for i in range(1, 151)]
    list_of_all_ad_urls = []
        
    try:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.map(fetch_and_parse_page, list_of_page_urls_for_rent)
            
            for result in results:
                if result:
                    list_of_all_ad_urls.extend(result)
                    
    except Exception as e:
        logging.error(f"Error fetching ad links: {e}")

    # logging.debug(f"Total ad URLs fetched: {len(list_of_all_ad_urls)}")
    return list_of_all_ad_urls