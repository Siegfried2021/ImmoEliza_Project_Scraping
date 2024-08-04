import json

def merge_json_lists(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    merged_list = [item for sublist in data for item in sublist]
    
    with open(output_file, 'w') as f:
        json.dump(merged_list, f, indent=4)

input_file = 'all_json_files_content_rent.json'
output_file = 'immoweb_properties_for_rent.json'

merge_json_lists(input_file, output_file)