import os

path = "C:/Users/Becky/Documents/acs_regions/msa_data/"
for root, dirs, files in os.walk(path, topdown=False):
    for file in dirs[1:]:
            os.chdir(path + file)
            for item in os.listdir(path + file  + '/'): # loop through items in dir
                if item.endswith(".geojson"): # check for ".geojson" extension
                    print(item)
                    os.system('mapshaper ' + item + ' -simplify 50% -o')
