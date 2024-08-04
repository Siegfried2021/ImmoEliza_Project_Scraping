import pandas as pd

def process_property_data(input_file, output_file):
    """
    Processes the JSON file containing property data to remove duplicates and save it as a CSV file.

    This function reads the property data from a JSON file that contains merged data for both properties for sale
    and rent, removes any duplicate entries, and saves the cleaned data into a CSV file. This step is done
    after scraping and consolidating the data to ensure that the final dataset is unique and suitable for analysis.

    Args:
        input_file (str): The path to the input JSON file containing the merged property data.
        output_file (str): The path to the output CSV file where the cleaned property data will be saved.
    """
    # Load the property data from the JSON file into a pandas DataFrame
    df_properties = pd.read_json(input_file)
    
    # Remove duplicate entries from the DataFrame
    df_properties = df_properties.drop_duplicates()
    
    # Reset the index of the DataFrame to ensure it is sequential
    df_properties.reset_index(drop=True, inplace=True)
    
    # Print the first few rows of the DataFrame to verify the results
    print(df_properties.head())
    
    # Save the cleaned DataFrame to a CSV file
    df_properties.to_csv(output_file, index=False)

# Define the input and output file paths
input_file = 'immoweb_properties_all.json'
output_file = 'immoweb_properties.csv'

# Call the function to process the property data and save it to a CSV file
process_property_data(input_file, output_file)
