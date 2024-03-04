import pandas as pd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Definición del modelo de datos
Base = declarative_base()

class City(Base):
    __tablename__ = 'parking_city'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    name_ascii = Column(String)
    alternative_name = Column(String)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    country_code = Column(String)

# Conexión a la base de datos (ajusta los parámetros según tu configuración)
engine = create_engine('postgresql://aparking:aparking@localhost:5432/aparking_db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Lectura del archivo CSV
df = pd.read_csv('/Users/sergiosantiago/Downloads/ES/cities.csv', header=None, names=['id', 'name', 'name_ascii', 'alternative_name', 'latitude', 'longitude', 'country_code'], delimiter=';')

# Conversión de las coordenadas a un punto WKT (Well-Known Text)
df['location'] = df.apply(lambda row: f'POINT({row.longitude} {row.latitude})', axis=1)

# Inserción de datos en la base de datos
for _, row in df.iterrows():
    city = City(id=row['id'], name=row['name'], name_ascii=row['name_ascii'], alternative_name=row['alternative_name'], location=row['location'], country_code=row['country_code'])
    session.add(city)

session.commit()
session.close()