import json

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

file1_path = 'immoweb_properties_for_sale.json'
file2_path = 'immoweb_properties_for_rent.json'

data1 = load_json_file(file1_path)
data2 = load_json_file(file2_path)

merged_data = data1 + data2

merged_file_path = 'immoweb_properties_all.json'
with open(merged_file_path, 'w') as merged_file:
    json.dump(merged_data, merged_file, indent=4)