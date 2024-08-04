import requests
from bs4 import BeautifulSoup
import json
import os
import logging
from filelock import FileLock

class RealEstateProperty:
    """
    Class representing a real estate property and its attributes.
    """
    def __init__(self, ad_url):
        """
        Initializes a RealEstateProperty object.

        Args:
            ad_url (str): The URL of the property ad.
        """
        self.ad_url = ad_url
        self.id = None
        self.sales_type = None
        self.post_code = None
        self.locality = None
        self.property_type = None
        self.price = None
        self.construction_year = None
        self.living_area = None
        self.bedrooms = None
        self.floor = None
        self.facades = None
        self.surface_plot = None
        self.kitchen_type = None
        self.furnished = None
        self.terrace = None
        self.surface_terrace = None
        self.surface_garden = None
        self.building_state = None
        self.swimming_pool = None
        self.basement = None
        self.energy = None
        self.initialize_base_attributes()
        
    def initialize_base_attributes(self):
        """
        Initializes base attributes from the ad URL.
        """
        list_of_first_items = self.ad_url.split('/')
        self.id = list_of_first_items[-1]
        self.post_code = list_of_first_items[-2]
        self.locality = list_of_first_items[-3]
        self.sales_type = list_of_first_items[-4]
        self.property_type = list_of_first_items[-5]
        
    def page_scraper(self):
        """
        Scrapes the property details from the ad page.
        """
        headers = {"User-agent": "mathieu", "Authorization": "mathieu2"}
        response = requests.get(self.ad_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        p_price = soup.find('p', class_='classified__price')
        if p_price:
            price_span = p_price.find('span', class_='sr-only')
            if price_span:
                self.price = price_span.get_text().replace("€", "").strip()
                
        th_construction_year = soup.find('th', string=lambda text: text and 'Construction year' in text)
        if th_construction_year:
            self.construction_year = int(th_construction_year.find_next('td').contents[0].strip())
        
        th_living_area = soup.find('th', string=lambda text: text and 'Living area' in text)
        if th_living_area:
            self.living_area = int(th_living_area.find_next('td').contents[0].strip())
            
        th_bedrooms = soup.find('th', string=lambda text: text and 'Bedrooms' in text)
        if th_bedrooms:
            self.bedrooms = int(th_bedrooms.find_next('td').contents[0].strip())
        
        th_floor = soup.find('th', string=lambda text: text and 'Floor' in text)
        if th_floor:
            self.floor = th_floor.find_next('td').contents[0].strip()

        th_facades = soup.find('th', string=lambda text: text and 'Number of frontages' in text)
        if th_facades:
            self.facades = int(th_facades.find_next('td').contents[0].strip())

        th_surface_plot = soup.find('th', string=lambda text: text and 'Surface of the plot' in text)
        if th_surface_plot:
            self.surface_plot = int(th_surface_plot.find_next('td').contents[0].strip())

        th_kitchen = soup.find('th', string=lambda text: text and 'Kitchen type' in text)
        if th_kitchen:
            self.kitchen_type = th_kitchen.find_next('td').contents[0].strip()

        th_furnished = soup.find('th', string=lambda text: text and 'Furnished' in text)
        if th_furnished:
            furnished_text = th_furnished.find_next('td').contents[0].strip()
            self.furnished = True if furnished_text == 'Yes' else False

        th_terrace = soup.find('th', string=lambda text: text and 'Terrace' in text)
        if th_terrace:
            terrace_text = th_terrace.find_next('td').contents[0].strip().lower()
            if terrace_text == 'yes':
                self.terrace = True
            elif terrace_text == 'no:':
                self.terrace = False

        th_surface_terrace = soup.find('th', string=lambda text: text and 'Terrace surface' in text)
        if th_surface_terrace:
            self.surface_terrace = int(th_surface_terrace.find_next('td').contents[0].strip())
            self.terrace = True

        th_surface_garden = soup.find('th', string=lambda text: text and 'Garden surface' in text)
        if th_surface_garden:
            self.surface_garden = int(th_surface_garden.find_next('td').contents[0].strip())

        th_building_state = soup.find('th', string=lambda text: text and 'Building condition' in text)
        if th_building_state:
            self.building_state = th_building_state.find_next('td').contents[0].strip()

        th_swimming_pool = soup.find('th', string=lambda text: text and 'Swimming pool' in text)
        if th_swimming_pool:
            swimming_pool_text = th_swimming_pool.find_next('td').contents[0].strip()
            self.swimming_pool = True if swimming_pool_text == 'Yes' else False
            
        th_basement = soup.find('th', string=lambda text: text and 'Basement' in text)
        if th_basement:
            basement_text = th_basement.find_next('td').contents[0].strip()
            self.basement = True if basement_text == 'Yes' else False

        th_energy = soup.find('th', string=lambda text: text and 'Energy class' in text)
        if th_energy:
            self.energy = th_energy.find_next('td').contents[0].strip()

    def to_dict(self):
        """
        Converts the property attributes to a dictionary.

        Returns:
            dict: Dictionary representation of the property attributes.
        """
        return {
            "id": self.id,
            "post_code": self.post_code,
            "locality": self.locality,
            "property_type": self.property_type,
            "sales_type": self.sales_type,
            "price": self.price,
            "construction_year": self.construction_year,
            "living_area": self.living_area,
            "bedroom number": self.bedrooms,
            "floor": self.floor,
            "facades": self.facades,
            "surface_plot": self.surface_plot,
            "kitchen_type": self.kitchen_type,
            "furnished": self.furnished,
            "terrace": self.terrace,
            "surface_terrace": self.surface_terrace,
            "surface_garden": self.surface_garden,
            "building_state": self.building_state,
            "swimming_pool": self.swimming_pool,
            "basement": self.basement,
            "energy": self.energy
        }

    def save_to_json(self, province):
        """
        Saves the property data to a JSON file.

        Args:
            province (str): The province for which to save the property data.
        """
        property_data = self.to_dict()
        filename = f"properties_{province}_rent.json"
        try:
            lock = FileLock(f"{filename}.lock")
            with lock:
                if os.path.exists(filename):
                    with open(filename, 'r+') as file:
                        data = json.load(file)
                        data.append(property_data)
                        file.seek(0)
                        json.dump(data, file, indent=4)
                else:
                    with open(filename, 'w') as file:
                        json.dump([property_data], file, indent=4)
        except IOError as e:
            logging.error(f"Error saving property {self.id} to {filename}: {e}")
