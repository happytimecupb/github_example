import pandas as pd

def convert_currency(val):
    """
    Convert the string number value to a float
     - Remove $
     - Remove commas
     - Convert to float type
     - Remove ' years'
    """
    new_val = val.replace(',','').replace('$', '').replace('years','')
    return float(new_val)

county = 'Travis'
csv_file = county +'-County-Data.csv'
#csv_file = 'HARRIS-County-Data.csv'

data = pd.read_csv(csv_file)
data = data.drop(data.columns[0], axis=1)

cols =['Zip Code','Latitude', 'Longitude',
       'Current Population', '2010 Population',
       'Households per ZIP Code', 'Average House Value',
       'Avg. Income Per Household', 'Persons Per Household',
       'White Population', 'Black Population', 'Hispanic Population',
       'Asian Population', 'American Indian Population', 'Hawaiian Population',
       'Other Population', 'Male Population', 'Female Population',
       'Median Age', 'Male Median Age', 'Female Median Age',
       '# Residential Mailboxes', '# Business Mailboxes',
       'Total Delivery Receptacles', 'Number of Businesses']
data_study = data[cols]

#remove '$',',','years' and change data type.
for col in data_study.columns:
    try:
        data_study[col] = data_study[col].apply(convert_currency)
    except:
        continue
    if('Population' in col):
        data_study[col]=data_study[col].astype(int)

#data_study.to_csv('HARRIS-County-Study-Data-with-0-Population.csv')
print(data_study.shape)

#remove row with zero population.
data_study = data_study[data_study['Current Population'] != 0]
data_study = data_study[data_study['2010 Population'] != 0]
print(data_study.shape)

#data_study.to_csv('HARRIS-County-Study-Data.csv')
data_study.to_csv(county+'-County-Study-Data.csv')

import folium # map rendering library

lat_harris = 29.7605059
lon_harris = -95.3588269

map_harris = folium.Map(location=[lat_harris, lon_harris], zoom_start=10)

# add markers to map
for lat, lng, zip_code in zip(data_study['Latitude'], data_study['Longitude'], data_study['Zip Code']):
    label = 'zip-{}, Harris'.format(zip_code)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_harris)

map_harris;