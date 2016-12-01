import pandas as pd
import numpy as np

#read in MSA state/county crosswalk
msa_guide = pd.read_csv('C:/Users/Becky/Documents/acs_regions/msa_guide.csv', index_col=0, dtype={'FIPSState Code':str, 'FIPSCountyCode':str, 'CBSA Code':str})

#returns a list of the counties in the msa in the form of [[state FIPS code, county FIPS code], ...]
def get_msa(msa_code):
    local = msa_guide.loc[msa_code, 'FIPS State Code':'FIPS County Code']
    # if there is only one county in the msa, "local" will be a series and needs to be converted to a dataframe
    if isinstance(local, pd.Series):
        local = pd.Series.to_frame(local)
        local = local.transpose() 
    county_list = []
    index = 0
    while index < len(local['FIPS State Code']):
        short_list = [(local['FIPS State Code'][index]), (local['FIPS County Code'][index])]
        county_list.append(short_list)
        index+=1
    return county_list

#returns an array containing all of the unique msa codes
def get_values():
    values = msa_guide.index.tolist()
    values = np.unique(values)
    values = [str(i) for i in values]
    return values
    
#returns an array containing all of the unique msa names
def get_names():
    names = msa_guide.CBSATitle.tolist()
    names = np.unique(names)
    return names