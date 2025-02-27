# ImmoEliza - Step 1: Web Scraping Real Estate Data

## Project Overview

This project involves scraping real estate property data from a website, processing the data, and saving it into a consolidated format for further analysis. The goal is to collect detailed property listings for both sale and rent, clean the data, and prepare it for analysis in a structured CSV format.

## Project Files

### 1. `pages_ads.py`

**Purpose**: Fetches web page links containing property ads and parses them to extract individual property URLs.

**Key Functions**:
- `fetch_page(url)`: Retrieves the HTML content of a web page given its URL.
- `parse_page_for_ads(html)`: Parses the HTML to find and extract property ad URLs.
- `fetch_and_parse_page(url)`: Combines fetching and parsing of a single page.
- `fetch_and_parse_ad_links(province)`: Retrieves and parses all property ad links for a specific province using multiprocessing.

**Usage**:
- This script is used to gather URLs for property ads by scraping multiple pages of listings.

### 2. `property_features.py`

**Purpose**: Fetches detailed features of each property from individual ad pages and saves them to a JSON file.

**Key Classes and Methods**:
- `RealEstateProperty`: A class that models a real estate property and contains methods to scrape and save its features.
  - `__init__(self, ad_url)`: Initializes the property with the ad URL and basic attributes.
  - `page_scraper(self)`: Scrapes the property details from the ad page.
  - `to_dict(self)`: Converts the property data into a dictionary format.
  - `save_to_json(self, province)`: Saves the property data to a JSON file with a province-specific filename.

**Usage**:
- This script is responsible for collecting detailed property information from each ad URL and saving it to a JSON file for later processing.

### 3. `main.py`

**Purpose**: Coordinates the entire scraping process, manages parallel processing of property ad URLs, and consolidates the data into JSON files.

**Key Functions**:
- `process_ad_url(province, ad_url)`: A helper function that initializes a `RealEstateProperty` object, scrapes property details from the ad URL, and saves them to a JSON file.
- `main()`: Manages the scraping process by fetching property ad URLs for each province and processing them in parallel. Handles the coordination of scraping, data collection, and file management.

**Usage**:
- This script is the entry point for initiating the scraping process. It:
  - Fetches property ad URLs for specified provinces.
  - Uses multiprocessing to handle multiple ad URLs in parallel.
  - Calls the `process_ad_url` function to scrape and save property details for each URL.

### 4. `merge_lists.py`

**Purpose**: Merges nested lists of JSON objects from an input file into a single list and writes it to an output file.

**Key Function**:
- `merge_json_lists(input_file, output_file)`: Loads nested lists from the specified JSON file, flattens them into a single list, and saves the result to another JSON file.

**Usage**:
- This script is used to consolidate property data from multiple province-specific JSON files into a single JSON file for properties for rent or sale.

### 5. `merge_files.py`

**Purpose**: Merges JSON files containing property data for sale and rent into a single JSON file.

**Key Functions**:
- `load_json_file(file_path)`: Loads a JSON file and returns its content as a list of dictionaries.

**Usage**:
- This script combines property data from separate JSON files for sale and rent into one consolidated JSON file.

### 6. `create_dataframe.py`

**Purpose**: Processes the JSON file containing merged property data to remove duplicates and save it as a CSV file.

**Key Functions**:
- `process_property_data(input_file, output_file)`: Loads JSON data, removes duplicate entries, resets the index, and saves the cleaned data to a CSV file.

**Usage**:
- This script cleans the merged JSON data by removing duplicates and converts it into a CSV format for analysis.

## Requirements

- **Python 3.x**: Ensure Python 3 is installed on your system.
- **Libraries**:
  - `requests`: For making HTTP requests to fetch web pages.
  - `beautifulsoup4`: For parsing HTML content.
  - `pandas`: For data manipulation and conversion to CSV.
  - `multiprocessing`: For parallel processing of data.
  - `filelock`: For ensuring file access is managed correctly during concurrent writes.

## Usage

### Fetch and Parse Ad Links

- **Run** `main.py` to start the scraping process.
  - This will collect all property ad URLs and save detailed property information in JSON files.

### Merge JSON Files

- **Run** `merge_lists.py` to merge JSON files for rent data into a single JSON file.
- **Run** `merge_files.py` to consolidate data from separate JSON files for sale and rent into a single JSON file.

### Process and Convert Data

- **Run** `create_dataframe.py` to clean the data and convert it from JSON to CSV format, making it ready for analysis.