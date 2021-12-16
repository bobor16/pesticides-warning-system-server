import os
from osgeo import gdal

input_directory = 'C:/Users/thoma/Desktop/input_folder/'
ouput_directory = 'C:/Users/thoma/Desktop/output_folder/'


for filename in os.listdir(input_directory):
    output_filename = os.path.splitext(filename)[0] + '_tile_'

    tile_size_x = 5490
    tile_size_y = 5490

    ds = gdal.Open(input_directory + filename)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
            com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(input_directory) + str(filename) + " " + str(ouput_directory) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
            os.system(com_string)