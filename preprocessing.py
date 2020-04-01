import pandas as pd
import re

codes = pd.read_csv("./data/London_District_codes.csv")
socio = pd.read_spss("./data/London_ward_data_socioeconomic.sav")
health = pd.read_sas("./data/london_ward_data_health.sas7bdat",
                     format='sas7bdat', encoding='latin1')
env = pd.read_csv("./data/London_ward_data_environment.csv")
demo = pd.read_csv("./data/London_ward_data_demographics.dat", delimiter='\t')

socio['Districtcode'] = socio['Wardcode'].str[:-2]
socio_env = pd.merge(socio, env, on='Wardcode')

codes['Districtcode'] = codes['Districtcode']\
    .replace(r'\s', '', regex=True)

health[
    ['District',
     'Ward',
     'remove',
     'remove']
] = health['Wardname'].str.split('-', expand=True)
health['District'] = health['District'].str[:-1]
health = health.drop('remove', axis=1)
total_df = pd.merge(socio_env, codes, on='Districtcode')
total_df = pd.merge(total_df, health, on='District')

demo[
    ['District',
        'Ward',
        'remove',
        'remove']
] = demo['Wardname'].str.replace('&', 'and', regex=True)\
    .str.split('-', expand=True)

# group to district level using mean values
demo = demo.drop('remove', axis=1)
demo['District'] = demo['District'].str[:-1]

total_df = pd.merge(total_df, demo, on='Wardname')
total_df.to_csv("./data/derived/combined_df.csv")
