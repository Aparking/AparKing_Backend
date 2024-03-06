import os
import django
import pandas as pd
from tqdm import tqdm
import threading
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AparKing_Backend.settings")
django.setup()

from django.contrib.gis.geos import Point
from apps.parking.models import City

def progress_bar(duration, step=0.1, final_delay=1):
    with tqdm(total=100, desc="Inserting cities") as pbar:
        increment = 100 / (duration / step)
        for i in range(int(duration / step)):
            time.sleep(step)
            if pbar.n + increment >= 99:
                pbar.update(99 - pbar.n)
                break
            else:
                pbar.update(increment)
        
        time.sleep(final_delay)
        pbar.update(100 - pbar.n)

def import_cities(file_path):
    if City.objects.exists():
        print("Los datos ya existen en la base de datos. Omitiendo la importación.")
        return
    
    col_names = ['id', 'name', 'name_ascii', 'alternative_name', 'latitude', 'longitude', 'country_code']
    df = pd.read_csv(file_path, header=None, names=col_names, delimiter=';')
    
    cities_to_create = []

    print('Creating cities')
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing cities"):
        location = Point(float(row['longitude']), float(row['latitude']))
        city = City(
            id=row['id'],
            name=row['name'],
            name_ascii=row['name_ascii'],
            alternative_name=row['alternative_name'],
            location=location,
            country_code=row['country_code']
        )
        cities_to_create.append(city)
    
    progress_thread = threading.Thread(target=progress_bar, args=(10, 0.1, 2.5))
    progress_thread.start()
    
    City.objects.bulk_create(cities_to_create)
    
    progress_thread.join()
    print(f"{len(cities_to_create)} cities added to the database successfully.")

if __name__ == '__main__':
    csv_file_path = './cities.csv'
    import_cities(csv_file_path)
