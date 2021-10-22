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

longitude = 55.356173
latitude = 10.391019
# 55.356173, 10.391019
m = folium.Map([longitude, latitude], zoom_start=11)
boundary = gpd.read_file(r'map.geojson')
folium.GeoJson(boundary).add_to(m)
m

print(m)

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

# bands = r'/L2A_T51JYN_A023938_20211006T014042/IMG_DATA/R10m'
blue = rasterio.open('src\T31XED_20211009T130949_B02_10m.jp2')
green = rasterio.open('src\T31XED_20211009T130949_B03_10m.jp2')
red = rasterio.open('src\T31XED_20211009T130949_B04_10m.jp2')
with rasterio.open('image_name.tiff', 'w', driver='Gtiff', width=blue.width, height=blue.height, count=3, crs=blue.crs, transform=blue.transform, dtype=blue.dtypes[0]) as rgb:
    rgb.write(blue.read(1), 3)
    rgb.write(green.read(1), 2)
    rgb.write(red.read(1), 1)
    rgb.close()

check = rasterio.open('image_name.tiff')
check.crs


bound_crs = boundary.to_crs({'init': 'epsg:32631'})
with rasterio.open("image_name.tiff") as src:
    out_image, out_transform = mask(src,
                                    bound_crs.geometry, crop=True)
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

with rasterio.open("masked_image.tif", "w", **out_meta) as final:
    final.write(out_image)

src = rasterio.open(r'.../masked_image.tif')
plt.figure(figsize=(6, 6))
plt.title('Final Image')
plot.show(src, adjust='linear')
