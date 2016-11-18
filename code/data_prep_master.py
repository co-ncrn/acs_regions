import pandas as pd
import numpy as np
import copy
import cenpy as cen
#import get_codes

data_path = 'C:/Users/Becky/Documents/acs_research/B_files/censusData/'
    
def get_data(scenario, fips, geo_name, geos='tract', api=True):
    #general scenario variables
    if scenario == 'gen_count':
        cols = ['B01003_001']
    elif scenario == 'gen_prop':
        cols = ['B25002_002', 'B25002_001', 'B11001_003', 'B11001_001', 'B16010_041', 'B16010_001', 'B07003_004', 'B07003_001', 
                'B03002_003', 'B03002_001', 'B03002_004', 'B03002_001', 'B03002_012', 'B03002_001', 'B09001_001', 'B01003_001', 
                'B09020_001', 'B01003_001']
    elif scenario == 'gen_ratio':
        cols = ['B25019_001', 'B25001_001', 'B19025_001', 'B25002_002', 'B25008_001', 'B25002_002']
    elif scenario == 'trans_count':
        cols = ['B01003_001']
    elif scenario == 'trans_prop':
        cols = ['B08101_009', 'B08101_001', 'B08101_025', 'B08101_001']
    elif scenario == 'trans_ratio':
        cols = ['B25046_001', 'B01003_001', 'B08013_001', 'B08134_001']
    elif scenario == 'hous_count':
        cols = ['B01003_001']
    elif scenario == 'hous_prop':
        cols = ['B25002_002', 'B25002_001', 'B25003_002', 'B25003_001', 'B25003_003', 'B25003_001', 'B25024_002', 'B25024_001']
    elif scenario == 'hous_ratio':
        cols = ['B25019_001', 'B25001_001', 'B25082_001', 'B25003_002', 'B25065_001', 'B25003_003']
    elif scenario == 'pov_count':
        cols = ['B01003_001']
    elif scenario == 'pov_prop':
        cols = ['B17006_016', 'B17006_001', 'B17001_031', 'B17001_001', 'B23025_004', 'B23025_003']
    elif scenario == 'pov_ratio':
        cols = ['B25089_001', 'B25120_002', 'B25065_001', 'B25120_005']
    elif scenario == 'sovi_count':
        cols = []
    elif scenario == 'sovi_ratio':
        cols = ['B25008_001', 'B25002_002', 'B19025_001', 'B25008_001', 'B19001_017', 'B11001_001', 
                'B25079_001', 'B25080_001', 'B25082_001', 'B25108_001', 'B25110_001', 'B25003_002', 
                'B25065_001', 'B25066_001', 'B25067_001', 'B25112_001', 'B25114_001', 'B25070_001', 'B01003_001']
                #'B01003_001']
                #Final ratio pair variable is added from geographic data below
    elif scenario == 'sovi_prop':
        cols = ['B03002_004', 'B03002_001', 'B03002_005', 'B03002_001', 'B03002_006', 'B03002_001', 'B03002_012', 'B03002_001',
                'B25003_003', 'B25002_001', 'B09020_021', 'B01003_001', 'B01001_026', 'B01003_001', 'B11001_006', 'B11001_001',
                'B25002_003', 'B25002_001', 'B16010_002', 'B16010_001', 'C24050_002', 'C24050_001', 'C24050_029', 'C24050_001',
                'B08201_002', 'B08201_001', 'B17021_002', 'B17021_001', 'B25024_010', 'B25024_001', 'C24010_038', 'C24010_001',
                'B19055_002', 'B19055_001', 'B09002_002', 'B09002_001', 'B06001_002', 'B09020_001', 'B01003_001',
                'B06007_005', 'B06007_008', 'B06007_001', 'B23022_025', 'B23022_049', 'B23022_001']
    elif scenario == 'income':
        cols = ['B06011_001']
    base_file_name = data_path+geo_name+'/'+geo_name+'_'+geos+'_'+scenario
    if api:
        # sort out the column names
        cols_ests = [i+'E' for i in cols]
        cols_moes = [i+'M' for i in cols]
        cols_all_data = cols_ests + cols_moes
        cols_all_data.append('B11001_001E')  # always pull total households
        cols_all_data = list(set(cols_all_data))  # get the unique column names
        cols_all = copy.copy(cols_all_data)
        cols_all.extend(['NAME', 'GEOID'])
        # API connection
        api_key = '19809d94f2ffead8a50814ec118dce7c5a987bfd'  # rebecca's census API key
        #api_key = '2ea3c1b17b3c1b907849cfaa1a04c51f4d0a19bf'  # folch's census API key        
        api_database = 'ACSSF5Y2012'  # ACS 2008-2012
        api_conn = cen.base.Connection(api_database)
        api_conn.set_mapservice('tigerWMS_Census2010')
        api_conn.mapservice
        # pull column info from API
        cols_detail = api_conn.variables.ix[cols_all].label.to_dict()        
        cols_detail = pd.DataFrame.from_dict(cols_detail, orient='index')
        # pull the data from the API
        data = pd.DataFrame()
        geodata = pd.DataFrame()
        for state, county in fips:
            if county == 'all':
                data = data.append(api_conn.query(cols_all, geo_unit=geos+':*', geo_filter={'state':state}, apikey = api_key))                
                if scenario == 'sovi_ratio':
                    geodata = geodata.append(api_conn.mapservice.query(layer = 14, where = 'STATE=%s' % state, pkg='geopandas', apikey=api_key))
            else:
                data = data.append(api_conn.query(cols_all, geo_unit=geos+':*', geo_filter={'state':state, 'county':county}, apikey = api_key)) 
                if scenario == 'sovi_ratio':
                    geodata = geodata.append(api_conn.mapservice.query(layer = 14, where = 'STATE=%s' % state + ' and COUNTY=%s' % county, pkg='geopandas', apikey=api_key))
        # convert dataframe index to the clean FIPS code prepended with 'g'
        index = 'g' + data.GEOID
        if geos=='tract':
            index = index.str.replace('14000US','')
        elif geos=='county':
            index = index.str.replace('05000US','')
        data.index = index
        if scenario == 'sovi_ratio':
            geodata = geodata[['AREALAND', 'GEOID']]
            geodata.AREALAND = geodata.AREALAND / 2589988.11
            geodata['GEOID'] = 'g' + geodata.GEOID
            data['agg_hs_val'] = data['B25079_001E']
            data['agg_hs_val'] = data['agg_hs_val'].fillna(data['B25080_001E'])
            data['agg_hs_val'] = data['agg_hs_val'].fillna(data['B25082_001E'])
            data['agg_hs_val'] = data['agg_hs_val'].fillna(data['B25108_001E'])
            data['agg_hs_val'] = data['agg_hs_val'].fillna(data['B25110_001E'])
            data['agg_rent'] = data['B25065_001E']
            data['agg_rent'] = data['agg_rent'].fillna(data['B25066_001E'])
            data['agg_rent'] = data['agg_rent'].fillna(data['B25067_001E'])
            data['agg_rent'] = data['agg_rent'].fillna(data['B25112_001E'])
            data['agg_rent'] = data['agg_rent'].fillna(data['B25114_001E'])
            data['agg_hs_val'] = data['B25079_001M']
            data['agg_hs_val'] = data['agg_hs_val'].fillna(data['B25080_001M'])
            data['agg_hs_val'] = data['agg_hs_val'].fillna(data['B25082_001M'])
            data['agg_hs_val'] = data['agg_hs_val'].fillna(data['B25108_001M'])
            data['agg_hs_val'] = data['agg_hs_val'].fillna(data['B25110_001M'])
            data['agg_rent'] = data['B25065_001M']
            data['agg_rent'] = data['agg_rent'].fillna(data['B25066_001M'])
            data['agg_rent'] = data['agg_rent'].fillna(data['B25067_001M'])
            data['agg_rent'] = data['agg_rent'].fillna(data['B25112_001M'])
            data['agg_rent'] = data['agg_rent'].fillna(data['B25114_001M'])
        data[cols_all_data] = data[cols_all_data].apply(pd.to_numeric)        
        # organize output dataframes and add multiindex column headers
        if scenario == 'sovi_prop':
            data['B06001_002E'] = data['B06001_002E'] + data['B09020_001E']
            data['B06007_005E'] = data['B06007_005E'] + data['B06007_008E']
            data['B23022_025E'] = data['B23022_025E'] + data['B23022_049E']
            data['B06001_002M'] = np.sqrt((data['B06001_002M'])**2 + (data['B09020_001M'])**2)
            data['B06007_005M'] = np.sqrt((data['B06007_005M'])**2 + (data['B06007_008M'])**2)
            data['B23022_025M'] = np.sqrt((data['B23022_025M'])**2 + (data['B23022_049M'])**2)   
        output_ests = data[cols_ests]
        output_moes = data[cols_moes]
        if scenario == 'sovi_prop':
            output_ests = output_ests.rename(columns = {'B23022_025E':'B23022_025E_B23022_049E',
                                          'B06007_005E':'B06007_005E_B06007_008E',
                                          'B06001_002E':'B06001_002E_B09020_001E'}) 
            output_moes = output_moes.rename(columns = {'B23022_025M':'B23022_025M_B23022_049M',
                                          'B06007_005M':'B06007_005M_B06007_008M',
                                          'B06001_002M':'B06001_002M_B09020_001M'})
            output_ests = output_ests.drop(['B09020_001E', 'B06007_008E', 'B23022_049E'], axis=1)
            output_moes = output_moes.drop(['B09020_001M', 'B06007_008M', 'B23022_049M'], axis=1)
        #identify tracts without households
        empty_tracts = data[data.B11001_001E == 0]
        empty_tracts = empty_tracts.index.values
        #adjust annual variables
        if scenario == 'pov_ratio':
            #multiply values by 12
            output_ests['B25089_001E'] = output_ests['B25089_001E'].mul(12) 
            output_ests['B25065_001E'] = output_ests['B25065_001E'].mul(12) 
            output_moes['B25089_001M'] = output_moes['B25089_001M'].mul(12) 
            output_moes['B25065_001M'] = output_moes['B25065_001M'].mul(12) 
        #write results to hard drive
        if scenario=='sovi_ratio': 
            output_ests = output_ests.merge(geodata, left_index=True, right_on='GEOID')
            output_ests = output_ests.set_index('GEOID')
            output_ests = output_ests.rename(columns={"AREALAND":"AREALANDE"})
            output_moes['AREALANDM'] = 0
            output_ests = output_ests.drop(['B25065_001E', 'B25066_001E', 'B25067_001E', 'B25112_001E', 'B25114_001E', 
                                            'B25079_001E', 'B25080_001E', 'B25082_001E', 'B25108_001E', 'B25110_001E'], axis=1)
            output_moes = output_moes.drop(['B25079_001M', 'B25080_001M', 'B25082_001M', 'B25108_001M', 'B25110_001M',
                                            'B25065_001M', 'B25066_001M', 'B25067_001M', 'B25112_001M', 'B25114_001M'], axis=1)
        output_ests.to_csv(base_file_name+'_ests.csv') 
        output_moes.to_csv(base_file_name+'_moes.csv') 
        cols_detail.to_csv(base_file_name+'_columns.csv', header=False)
        np.savetxt(base_file_name+'_empty.csv', empty_tracts, delimiter=',', fmt='%s')    
    # always return data read from hard drive
    output_ests = pd.read_csv(base_file_name+'_ests.csv', index_col=0) 
    output_moes = pd.read_csv(base_file_name+'_moes.csv', index_col=0) 
    cols_detail = pd.read_csv(base_file_name+'_columns.csv', header=None, index_col=0)
    empty_tracts = np.genfromtxt(base_file_name+'_empty.csv', delimiter=',', dtype=str)
    empty_tracts = np.atleast_1d(empty_tracts)
    empty_tracts = empty_tracts.tolist()
    return output_ests, output_moes, cols_detail, empty_tracts


#manual version:
#input MSA code to get corresponding list of lists of state and county FIPS codes
#codes = get_codes.get_msa('38900')

#output
#output_ests, output_moes, cols_detail, empty_tracts = get_data('trans_prop', 
#                                                 fips=codes,
#                                                 geo_name='38900',
#                                                 geos='tract', api=True)

