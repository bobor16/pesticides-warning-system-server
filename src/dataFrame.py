import folium
import geopandas as gpd
from sentinelsat.sentinel import SentinelAPI
import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
from osgeo import gdal
import config as cfg

m = folium.Map([latitude, longitude], zoom_start=11)
boundary = gpd.read_file(r'map.geojson')
folium.GeoJson(boundary).add_to(m)
m

footprint = None
for i in boundary['geometry']:
    footprint = i

user = cfg.user
password = cfg.password
api = SentinelAPI(user, password, 'https://apihub.copernicus.eu/apihub/')
products = api.query(footprint,
                     date=('20211001', '20211010'),
                     platformname='Sentinel-2',
                     processinglevel='Level-2A',
                     cloudcoverpercentage=(0, 20))

gdf = api.to_geodataframe(products)
gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
gdf_sorted


