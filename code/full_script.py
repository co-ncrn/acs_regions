# Regionalization script
# July 29, 2016
# Becky Davies, David Folch, Seth Spielman

#Depends on additional scripts: get_codes, acs_regionalization, extract_msas, data_prep_master, fullFunc
#Requires input docs: USA census tracts shapefile, MSA county crosswalk from OMB

import pysal as ps
import numpy as np
import pandas as pd
import geopandas as gp
import random
import acs_regionalization as ACS
import get_codes
import extract_msas as em
import data_prep_master as dpm
import fullFunc as ff
import os.path

# 0. User inputs
# Select the scenario to run
scenario = 'transportation'
count, all_types, scenario2 = ff.set_scenario(scenario)

# Get Codes uses the crosswalk to identify state and county FIPS codes
# within the selected MSA
values = get_codes.get_values()
# Manually enter an MSA FIPS code or slice the "values" list generated
# above to select a range of MSAs
values = ['19740']

# I. Generate shape files

# Extract MSAs constructs msa shape files from the master tracts file for the USA 
# The results are written to hard drive
em.get_shp(values)

# II. Generate data

# Runs through all unique msa codes to get data for each
for value in values:
    
    codes = get_codes.get_msa(value) 
    # Creates a new folder for the msa data if one does not already exist
    data_path = 'C:/Users/Becky/Documents/acs_research/B_files/censusData/' + value + '/'   
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    for var_type in all_types:    
        output_ests, output_moes, cols_detail, empty_tracts = dpm.get_data(scenario2 + '_' + var_type, 
                                                fips=codes,
                                                geo_name='%s' % value,
                                                geos='tract', api=True)                                       
    
    # III. Run regionalization         
    
    # Locations of input files   
    base_shp = 'C:/users/becky/documents/acs_research/B_files/msas/' + value + '/'
    base_data = 'C:/users/becky/documents/acs_research/B_files/censusData/' + value + '/'

    shp_map = gp.read_file(base_shp + '19740' + '.shp')
    w = ps.rook_from_shapefile(base_shp + '19740' + '.shp', idVariable='GEOID')
    
    # Adjustments for "islands" (census tracts with no neighbors)
    islands = ['13380','14740','15260','15380','15980', '48900','16700','18880','19820','20260',
              '25940','27340', '28140', '31080','33100','34820','34940','35840','35620',
              '36140','38940','39300', '39460', '41980','42660','45300','47260','48900']
    if value in islands:
        ff.isIsland(value, w)
    
    # Read in list of census tracts with no households to exclude
    exclude = open(base_data + value + '_tract_' + scenario2 + '_count_empty.csv')
    exclude = exclude.readlines()
    exclude = map(lambda x: x.replace('g', ''), exclude)
    exclude = map(lambda x: x.strip(), exclude)
    exclude = filter(None, exclude)
    tracts = shp_map.GEOID
    tract_list = tracts.tolist()
    exclude = [a for a in exclude if a in tract_list]
    
    # Special exceptions
    # Exclude Point Roberts in Bellingham, WA (it is connected to land in Canada only)
    if value == '13380':
        exclude.append('53073011000')
    # Exclude Boca Grande in Cape Coral, FL (it is connected to land outside of MSA)
    if value == '15980':
        exclude.append('12071090100')
    # Exclude Catalina Island off the LA coast
    if value == '31080':
        exclude.extend(['06037599100', '06037599000'])
    print exclude 

    # Read in the ACS estimates and standard errors
    population = pd.read_csv(base_data + value + '_tract_' + scenario2 + '_count_ests.csv', index_col=0)
    
    est_prop = pd.read_csv(base_data + value + '_tract_' + scenario2 + '_prop_ests.csv', index_col=0)
    moe_prop = pd.read_csv(base_data + value + '_tract_' + scenario2 + '_prop_moes.csv', index_col=0)
    prop_names = open(base_data + value + '_tract_' + scenario2 + '_prop_columns.csv')
    prop_names = prop_names.readline().split(',')

    est_ratio = pd.read_csv(base_data + value + '_tract_' + scenario2 + '_ratio_ests.csv', index_col=0)
    moe_ratio = pd.read_csv(base_data + value + '_tract_' + scenario2 + '_ratio_moes.csv', index_col=0)
    ratio_names = open(base_data + value + '_tract_' + scenario2 + '_ratio_columns.csv')
    ratio_names = ratio_names.readline().split(',')
        
    # Save order of rows in shapefile
    shp_order = shp_map['GEOID'].values
    shp_order = 'g' + shp_order
    shp_order = shp_order.tolist()
    
    # Order data file rows to match shapefile
    population = population.reindex(index = shp_order)
    est_prop = est_prop.reindex(index = shp_order)
    moe_prop = moe_prop.reindex(index = shp_order)
    est_ratio = est_ratio.reindex(index = shp_order)
    moe_ratio = moe_ratio.reindex(index = shp_order)
    
    # This may take up to four minutes to run depending on hardware speed
    shp = ps.open(base_shp + value + '.shp')
    random.seed(789)     # to ensure we get the same solution each time
    np.random.seed(789)  # to ensure we get the same solution each time
    try:
        print value + " regionalization started" + "\n"
        results = ACS.ACS_Regions(w=w,\
                            target_est_prop=est_prop.values,\
                            target_moe_prop=moe_prop.values,\
                            target_est_ratio=est_ratio.values,\
                            target_moe_ratio=moe_ratio.values,\
                            count_est=population.values,\
                            target_th_all=0.12,\
                            exclude=exclude,\
                            compactness=shp,\
                            cv_exclude_prop=0.05)
        print value, 'regionalization finished' + "\n"        
        
    except:
        print 'regionalization failed for ' + value + "\n"
    

    #IV. Generate Output
    
    # Rename computed variables for legibility
    results = ff.rename_vars(results, scenario)
    
    #Set detination folder
    output_path = 'C:/users/becky/documents/acs_research/C_results/' 
    
    if not os.path.exists(output_path + value + '/'):
        os.makedirs(output_path + value + '/')
        
    # Set prefix for output file names
    prefix = value + '_' + scenario2  + '_'
    
    # Read in moe data from results
    moe_population = pd.read_csv(base_data + value + '_tract_' + scenario2 + '_count_moes.csv', index_col=0) 
    moe_population = moe_population.reindex(index = shp_order)
    input_files = [population, moe_population, est_prop, moe_prop, est_ratio, moe_ratio]
    columns = [population.columns, moe_population.columns, est_prop.columns, moe_prop.columns, est_ratio.columns, moe_ratio.columns]
    
    # Designate path of prj file to copy for output shapefiles
    prj = base_shp + value + '.prj'
    
    # Generate input tract data in csv format
    all_inputs = ff.create_tractcsv(output_path + value + '/', results, input_files, columns, scenario, prefix)
    
    # Generate crosswalk between regions and tracts
    crosswalk = ff.create_crosswalk(output_path + value + '/', prefix, shp_map, results)
    
    # Generate output region data in csv format
    df = ff.create_regioncsv(output_path + value + '/', prefix, results, input_files, all_inputs, crosswalk)
    
    json_path = 'C:/users/becky/documents/acs_research/C_results/GeoJSON/' + value + '/'
    if not os.path.exists(json_path):
        os.makedirs(json_path)
        
    # Generate shapefiles and geojson
    ff.create_shapes(output_path + value + '/', prefix, results, shp_map, all_inputs, df, prj, json_path, value)
    
    # Generate associated weights matrix for region shapefile
    ff.create_weights(output_path + value + '/', prefix, w)
    
    # Style geojson
    ff.style_geojson(json_path + value + '_tract.geojson', 'id', 'tract')
    ff.style_geojson(json_path + prefix + 'region.geojson', 'RID', 'region')
    
    # Copy metadata file and data dictionary to output folder
    meta = '/Users/becky/documents/acs_web_reg/code/metadata.txt'
    dict1 = '/Users/becky/documents/acs_web_reg/code/dataDict.csv'
    metadata, dataDict = ff.meta(output_path + value + '/', meta, dict1)
    
    # Write results to .zip file
    fileList = [dataDict, metadata, output_path + value + '/' + prefix + 'crosswalk.csv', output_path + value + '/' + prefix + 'output_regions.csv',
                output_path + value + '/' + prefix + 'regions.shp', output_path + value + '/' + prefix + 'regions.shx', 
                output_path + value + '/' + prefix + 'regions.cpg', output_path + value + '/' + prefix + 'regions.dbf', 
                output_path + value + '/' + prefix + 'regions.prj', output_path + value + '/' + prefix + 'input_tracts.csv', 
                output_path + value + '/' + prefix + 'tracts.shp', output_path + value + '/' + prefix + 'tracts.shx', 
                output_path + value + '/' + prefix + 'tracts.cpg', output_path + value + '/' + prefix + 'tracts.dbf', 
                output_path + value + '/' + prefix + 'tracts.prj', output_path + value + '/' + prefix + 'weights_matrix.gal']
    archive = output_path + 'zips/' + value + '/' + prefix + 'results.zip'
    root = output_path + value + '/'
    path = output_path + 'zips/' + value + '/'
    ff.makeArchive(fileList, archive, root, path)
    