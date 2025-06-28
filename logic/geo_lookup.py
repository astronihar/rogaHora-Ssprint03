# logic/geo_lookup.py
import csv

def load_city_data(filepath="./data/Indian_Cities_Geo_Data.csv"):
    data = {}
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Strip header keys first
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}  # Clean both keys and values
            state = row['state']
            city = row['city']
            lat = float(row['lat'])
            lon = float(row['lon'])

            if state not in data:
                data[state] = {}
            data[state][city] = (lat, lon)
    return data
