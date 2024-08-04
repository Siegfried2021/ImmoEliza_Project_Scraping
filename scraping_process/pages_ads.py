import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import multiprocessing
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_page(url):
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: HTML content of the page if successful, None otherwise.
    """
    try:
        headers = {"User-agent": "mathieu", "Authorization": "mathieu2"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
 
        if response.status_code == 200:
            html = response.text
            return html
        else:
            logging.warning(f"Page {url} does not exist. Status code: {response.status_code}")
            return None
    except RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
        return None

def parse_page_for_ads(html):
    """
    Parses the HTML content to extract ad URLs.

    Args:
        html (str): HTML content of the webpage.

    Returns:
        list: List of ad URLs found on the page.
    """
    soup = BeautifulSoup(html, 'html.parser')
    h2_elements = soup.find_all('h2')
    list_ad_urls = []
    for h2 in h2_elements:
        a_element = h2.find('a', class_='card__title-link')
        if a_element and 'href' in a_element.attrs:
            ad_url = a_element['href']
            list_ad_urls.append(ad_url)
    return list_ad_urls

def fetch_and_parse_page(url):
    """
    Fetches the HTML content of a page and parses it for ad URLs.

    Args:
        url (str): The URL of the webpage to fetch and parse.

    Returns:
        list: List of ad URLs found on the page.
    """
    html = fetch_page(url)
    if html:
        page_ad_urls = parse_page_for_ads(html)
        return page_ad_urls
    else:
        return []

def fetch_and_parse_ad_links(province):
    """
    Fetches and parses all ad links for a given province.

    Args:
        province (str): The province for which to fetch and parse ad links.

    Returns:
        list: List of all ad URLs found for the province.
    """
    root_url_for_rent = 'https://www.immoweb.be/en/search/house-and-apartment/for-rent'
    # root_url_for_same = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale'
    list_of_page_urls_for_rent = [f"{root_url_for_rent}/{province}/province?countries=BE&page={i}&orderBy=relevance" for i in range(1, 151)]
    # list_of_page_urls_for_sale = [f"{root_url_for_sale}/{province}/province?countries=BE&page={i}&orderBy=relevance" for i in range(1, 151)]

    list_of_all_ad_urls = []
        
    try:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.map(fetch_and_parse_page, list_of_page_urls_for_rent)
            
            for result in results:
                if result:
                    list_of_all_ad_urls.extend(result)
                    
    except Exception as e:
        logging.error(f"Error fetching ad links: {e}")

    return list_of_all_ad_urls