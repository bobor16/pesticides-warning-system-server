import pandas as pd
from PIL import Image
import csv
from osgeo import gdal, osr
import matplotlib.pyplot as plt

#px creates a pixel array of the geotif file
im = Image.open(r"src\example.tif")
px = im.load()

#creates a csv file to to list x, y and grayscale of choosen pixels
f = open("src/waterPixels.csv", 'w', encoding='UTF8', newline='')
writer = csv.writer(f)
height, width = im.size
print(height, width)
print(height * width)


g = gdal.Open ( "src/example.tif" ) # Open the file for georeference

old_cs= osr.SpatialReference()
old_cs.ImportFromWkt(g.GetProjectionRef())

# create the new coordinate system
wgs84_wkt = """
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""
new_cs = osr.SpatialReference()
new_cs .ImportFromWkt(wgs84_wkt)

# create a transform object to convert between coordinate systems
transform = osr.CoordinateTransformation(old_cs,new_cs) 

#get the point to transform, pixel (0,0) in this case
width = g.RasterXSize
height = g.RasterYSize
gt = g.GetGeoTransform()

print(gt)
print(width, height)
minx = gt[0] + 1000*gt[1]
miny = gt[3] + width*gt[4] + height*gt[5]

print(minx, miny)

#get the coordinates in lat long
latlong = transform.TransformPoint(minx,miny) 
print('latlong = ')
print(latlong)


#loops through they pixel array of the geotif file
#check if color of the pixel is in the desired range (can be tuned)
#writes the x, y coordiate in the image and the grayscale color
for x in range(width):
  for y in range(height):
      if((53) > px[x, y] > (50)) :
        #gets the point to transform
        minx = gt[0] + x*gt[1]
        miny = gt[3] + y*gt[5]
        #get the coordinates in lat long
        latlong = transform.TransformPoint(minx,miny) 
        plt.plot(x,y, 'ro')
        writer.writerow([x, y, latlong])


lc = g.ReadAsArray() # Read raster data
# Now plot the raster data using gist_earth palette
plt.imshow ( lc, interpolation='nearest', vmin=0, cmap=plt.cm.gist_earth )
# Plot location of our area of interest as a red dot ('ro')
plt.xticks([])
plt.yticks([])
plt.show()