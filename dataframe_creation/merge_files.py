import json

def load_json_file(file_path):
    """
    Loads a JSON file and returns its content.

    This function is used to load JSON files containing property data that were scraped
    and saved during the web scraping process for properties either for sale or for rent.

    Args:
        file_path (str): The path to the JSON file to be loaded.

    Returns:
        list: The content of the JSON file as a list of dictionaries.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

# Define the file paths for the property data JSON files for sale and rent
file1_path = 'immoweb_properties_for_sale.json'
file2_path = 'immoweb_properties_for_rent.json'

# Load the property data from the JSON files
data1 = load_json_file(file1_path)
data2 = load_json_file(file2_path)

# Merge the data from the two JSON files into a single list
merged_data = data1 + data2

# Define the path for the merged JSON file
merged_file_path = 'immoweb_properties_all.json'

# Write the merged property data to the new JSON file
with open(merged_file_path, 'w') as merged_file:
    json.dump(merged_data, merged_file, indent=4)