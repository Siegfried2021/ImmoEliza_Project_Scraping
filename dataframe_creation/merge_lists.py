import json

def merge_json_lists(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    merged_list = [item for sublist in data for item in sublist]
    
    with open(output_file, 'w') as f:
        json.dump(merged_list, f, indent=4)

input_file = 'all_json_files_content_rent.json'
output_file = 'immoweb_properties_for_rent.json'

merge_json_lists(input_file, output_file)import json

def merge_json_lists(input_file, output_file):
    """
    Merges nested lists of JSON objects from an input file into a single list and writes it to an output file.

    This function is designed to process the output from the web scraping process where each province's
    property data is stored as a list of dictionaries in a nested list structure. The merged list contains 
    all property data in a flat list format, making it easier to work with for further data analysis or processing.

    Args:
        input_file (str): The path to the input JSON file containing a list of lists with property data.
        output_file (str): The path to the output JSON file where the merged list of property data will be saved.
    """
    # Open and read the input JSON file containing nested lists of property data
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Merge all nested lists of property data into a single list
    merged_list = [item for sublist in data for item in sublist]
    
    # Write the merged list of property data to the output JSON file
    with open(output_file, 'w') as f:
        json.dump(merged_list, f, indent=4)

# Define the input and output file paths based on the web scraping process output
input_file = 'all_json_files_content_rent.json'
output_file = 'immoweb_properties_for_rent.json'

# Call the function to merge JSON lists containing property data
merge_json_lists(input_file, output_file)
