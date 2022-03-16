"""
Importing and filtering data on Chicago's libraries, pharmacies,
    and murals for use in our software.

"""
from matplotlib.style import library
from sodapy import Socrata

import json
import pandas as pd

from library import Library
from pharmacy import Pharmacy
from murals import Mural

API_KEY = "9Qto0x2IrJoK0BwbM4NSKwpkr"

class DataPortalCollector: 

    def __init__(self):
        '''
        # COME BACK FOR DOCSTRING HERE # 
        '''
        # Unauthenticated client only works with public data sets. 
        self.client = Socrata("data.cityofchicago.org", API_KEY)
        
    def get_libraries(self):
        '''
        Pull the the data on libraries located in Chicago from Chicago Open Data Portal
            and save as a pandas dataframe
        Inputs:
            - none
        Returns:
            -  library_df: (pandas dataframe) a dataframe with name,
                latitude, longitude, and address of
                all libraries in Chicago
        '''
        
        results = self.client.get("x8fc-8rcq")
        library_df = pd.DataFrame.from_dict(results)
        
        return library_df

    def get_pharmacies(self):
        '''
        Pull the data on pharmacies located in Chicago from Chicago Open Data Portal
            and save as a pandas dataframe
        Inputs: 
            - none
        Returns:
            - pharmacy_df: (pandas dataframe) a dataframe with name,
                latitude, longitude, address, and open/closed status of all
                pharmacies in Chicago
        '''
        
        results = self.client.get("2et2-5aw3")
        pharmacy_df = pd.DataFrame.from_dict(results)
        
        return pharmacy_df


    def get_murals(self):
        '''
        '''
        
        results = self.client.get("we8h-apcf")
        print(results)
        print('')
        return 
        murals_df = pd.DataFrame.from_dict(results)
        
        return murals_df


def clean_libraries(dpc_class):
    '''
    '''

    libs = dpc_class.get_libraries()

    filter_data = libs[["name_", "address", "location"]]

    # split location column up
    split_location_col = [filter_data, pd.DataFrame(filter_data["location"].tolist()).iloc[:, :3]]
    split_location = pd.concat(split_location_col, axis=1).drop(['location', "human_address"], axis=1)
   
    # change column name
    split_location = split_location.rename(columns = {"name_": "name"})
    split_location["type"] = "library"
    
    return split_location


def clean_pharmacies(dpc_class):
    '''
    '''

    pharms = dpc_class.get_pharmacies()

    filter_data = pharms[["pharmacy_name", "address", "geocoded_column", "status"]]

    # split location column up into lat/lon
    split_location = pd.concat([filter_data, filter_data["geocoded_column"].apply(pd.Series)], axis=1)
    split_location = split_location[["pharmacy_name", "address", "status", "coordinates"]]
    split_location_list = pd.concat([split_location, split_location["coordinates"].apply(pd.Series)], axis=1)
    
    # fix coordinate column names
    split_location_list = split_location_list.rename(columns = {0: "lon", 1: "lat"})

    # only columns we want
    condensed = split_location_list[["pharmacy_name", "address", "lat", "lon", "status"]]

    # clean status column
    pharms_clean = condensed.copy()
    mask1 = (pharms_clean.status == "Open") | (split_location.status == "OPEN")
    mask2 = pharms_clean.status == "CLOSED"
    mask3 = pharms_clean.status == "Permanently closed"
    column = "status"
    pharms_clean.loc[mask1, column] = "open"
    pharms_clean.loc[mask2, column] = "closed"
    pharms_clean.loc[mask3, column] = "permanently closed"

    # change column name
    pharmacy_data = pharms_clean.rename(columns = {"pharmacy_name": "name"})
    pharmacy_data["type"] = "pharmacy"

    pharmacy_data.dropna(inplace = True)

    return pharmacy_data


def clean_murals(dpc_class):
    '''
    '''

    murals_df = dpc_class.get_murals()

    murals_df = murals_df[["artwork_title", "street_address", "lat", "lon"]]
    murals_df.rename(columns = {'artwork_title':'name', "street_address":'address'}, inplace = True)
    murals_df.dropna(inplace = True)

    return murals_df


# append THE TWO DATAFRAMES
def append_pandas():
    '''
    
    '''
    dpc = DataPortalCollector()

    library_data = clean_libraries(dpc)
    pharmacy_data = clean_pharmacies(dpc)
    murals_data = clean_murals(dpc)

    return (library_data, pharmacy_data, murals_data)


def get_data_dicts():

    lib, pharm, mur = append_pandas()

    lib_dict = lib.to_dict('records')
    pharm_dict = pharm.to_dict('records')
    mur_dict = mur.to_dict('records')

    return (lib_dict, pharm_dict, mur_dict)