import pandas as pd

df_properties = pd.read_json('immoweb_properties_all.json')

df_properties = df_properties.drop_duplicates()

df_properties.reset_index(drop=True, inplace=True)

print(df_properties.head())

df_properties.to_csv('immoweb_properties.csv', index=False)