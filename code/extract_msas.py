import pandas as pd
import numpy as np
import geopandas as gpd
import os.path

#open file with all US census tracts
allTracts = ('C:/Users/becky/Documents/acs_research/A_inputs/usa_2.shp')

#open shapefile
usa_tracts = gpd.read_file(allTracts)

#open msa crosswalk file as Pandas df
guide = pd.read_csv('C:/Users/becky/Documents/acs_research/A_inputs/msa_guide.csv', dtype={'FIPSStateCode':str, 'FIPSCountyCode':str, 'CBSACode':str})
#filter out micropolitan areas
guide = guide[guide.Metropolitan_Micropolitan_Statistical_Area == "Metropolitan Statistical Area"]

#list of unique msa codes 
#msas = guide['CBSACode'].unique()
 
#tract_code = usa_tracts.STATEFP + usa_tracts.COUNTYFP
guide['FIPSStateCode'] = guide['FIPSStateCode'].apply(lambda x: x.zfill(2))
guide['FIPSCountyCode'] = guide['FIPSCountyCode'].apply(lambda x: x.zfill(3))
for row in guide:
    guide['code'] = pd.Series(guide['FIPSStateCode']+guide['FIPSCountyCode'])
for row in usa_tracts:
    usa_tracts['code'] = pd.Series(usa_tracts['STATEFP']+usa_tracts['COUNTYFP'])

def get_shp(msas):
    #filter one msa at a time
    for msa in msas:
        guide2 = guide[guide.CBSACode==msa]
        match = usa_tracts[(usa_tracts['code'].isin(guide2['code']))]
        match.drop('code', axis=1)
        # Creates a new folder for the msa data if one does not already exist
        data_path = 'C:/Users/becky/Documents/acs_research/B_files/msas/' + msa + '/'   
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        match.to_file(data_path + msa + '.shp')