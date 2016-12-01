import geopandas as gpd
import json
import random
import geojson
#from shapely.geometry import shape


def convert_to_json(inputpath, outputpath):
    
    # Read in shapefile as Geopandas DF
    geoj = gpd.read_file(inputpath)

    # Convert Geopandas DF to JSON file
    with open(outputpath, 'w') as f:
        f.write(geoj.to_json())

def style_geojson(outputpath, typeID, geo):
    
    #Open JSON file as Python object
    with open(outputpath) as f:
        data = json.load(f)

    x = len(data['features'])
    
    # Iterate through all features (regions)
    for i in range(x): 
    
        # Add styling to polygon
        # Randomly color regions
        r = lambda: random.randint(0,255)
        color = ('#%02X%02X%02X' % (r(),r(),r()))
        r = color
        data['features'][i]['properties']['stroke'] = '#000066'
        data['features'][i]['properties']["fill"] = r
        data['features'][i]['properties']["stroke-width"] = 2 
        data['features'][i]['properties']["fill-opacity"] = .6
        data['features'][i]['properties']["stroke-opacity"] = 10
        '''         
        if geo == 'region':
           
            if i < 100: 
                # Find 'centroid' of polygon (actually a representative point within polygon)
                s = data['features'][i]['geometry']
                o = json.dumps(s)
                g1 = geojson.loads(o)
                g2 = shape(g1)
                center = g2.representative_point().coords[0]
        
                # Add marker feature at polygon 'centroid' 
                marker_dict = {"geometry": {"coordinates": [
                        center[0], center[1]], "type": "Point"},
                        "properties": {"marker-color": "#000000", 
                        "marker-size": "large", 
                        "marker-symbol": data['features'][i]['properties'][typeID]},
                        "type": "Feature"} 
    
                data['features'].append(marker_dict)
        '''      
    # Write back to file          
    with open(outputpath,"w") as f:
        json.dump(data, f, sort_keys=True)
