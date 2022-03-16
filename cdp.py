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
    split_location = split_location.rename(columns = {"name_": "name", "latitude": "lat", "longitude": "lon"})
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
    split_location_list = split_location_list.rename(columns = {0: "longitude", 1: "latitude"})

    # only columns we want
    condensed = split_location_list[["pharmacy_name", "address", "latitude", "longitude", "status"]]

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
    pharmacy_data = pharms_clean.rename(columns = {"pharmacy_name": "name", "latitude": "lat", "longitude": "lon"})
    pharmacy_data["type"] = "pharmacy"

    pharmacy_data.dropna(inplace = True)

    return pharmacy_data


def clean_murals(dpc_class):
    '''
    '''

    murals_df = dpc_class.get_murals()

    murals_df = murals_df[["artwork_title", "street_address", "latitude", "longitude"]]
    murals_df.rename(columns = {"artwork_title":"name", "street_address":"address", "latitude": "lat", "longitude": "lon"}, inplace = True)
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











###########################################################################################
# DELETE ROWS BELOW HERE LATER ############


    # first_col = split_location.pop("type")
    # # cop = split_location.copy()
    
    # split_location = split_location.insert(0, "type", first_col)
    # move type to front


# def obtain_libraries():
#     '''
#     Create an instance of the DataPortalClass to find all libraries
#         and return the dataframe of libraries (NOT SURE IF THIS SHOULD BE BROKEN INTO THIS SEPARATE FUNCTION)
#     Inputs:
#         - none
#     Returns:
#         - libs 
#     '''
#     dpc = DataPortalCollector()
#     libs = dpc.get_libraries()
#     print(type(libs))
#     return libs

# def obtain_pharmacies():
#     '''
#     '''
#     dpc = DataPortalCollector()
#     pharms = dpc.get_pharmacies()
#     return pharms





# # Converting to pandas dataframe 
# # put these functions in different file?
# # also combine to call function within function so we can make these generalized to pulling anyh
# # of the three datasets and then create them all in one overall function? 
# # would have to review how to call function in function

# def obj_dict(obj):
#     '''
#     '''
#     return obj.__dict__


# def to_json_libraries(obj):
#     '''
#     '''
#     ob_dict = obj_dict(obj)
#     dpc = DataPortalCollector()
#     libs = dpc.get_libraries()
    
#     # convert list to json
#     json_string = json.dumps(libs, default = ob_dict) #https://stackoverflow.com/questions/26033239/list-of-objects-to-json-with-python

#     return json_string

# def to_json_pharmacies(obj_dict):
#     '''
#     '''
#     dpc = DataPortalCollector()
#     libs = dpc.get_pharmacie()
#     # convert list to json
#     json_string = json.dumps(libs, default = obj_dict)
#     #print(json_string, "json_string")

#     return json_string

# def to_pandas(obj_dict):
#     '''
#     '''
#     dpc = DataPortalCollector()
#     libs = dpc.get_libraries()
#     #for lib in libs:
#     df = pd.DataFrame([x.as_dict() for x in libs])




# def to_pandas_libraries(obj_dict):
#     '''
#     '''
#     json_string = to_json_libraries(obj_dict)
#     libraries_pd = pd.read_json(json_string)
#     return libraries_pd

# def to_pandas_pharmacies(obj_dict):
#     '''
#     '''
#     json_string = to_json_pharmacies(obj_dict)
#     pharmacies_pd = pd.read_json(json_string)
#     return pharmacies_pd

# li = cdp.to_pandas(json_string, obj_dict)


# questions for ian - do we want to split coordinates into two columns,
# one for longitude/one for latitude? Currently some of these data frames do
# coordinates column = ("longitude, latitude") and others do ("latitude", "longitude")










# json_string = json.dumps(list_name, default=obj_dict)
# # loading in ipython3 # 

# dpc = DataPortalCollector()
# libs = dpc.get_libraries()
# pharms = dpc.get_pharmacie()
# for lib in libs:
#     print(type(print(lib)))


# # how to call this:
# ipython libviewer.py -- --limit=1000

# view things in dataframe
#li.columns
# li.loc[:,"name"]
#li.loc[:,"coordinates"]



# def _decode_library_data(dct):
#     '''
#     '''
#     #First check that all required attributes are inside the dictionary 
#     if all (key in dct for key in ["name_","location","address"]):
#         return Library(dct["name_"], (dct["location"]['latitude'], dct["location"]['longitude']), dct["address"])
#     return dct  

# def _decode_pharmacy_data(dct): 
#     '''
#     '''
#     if all (key in dct for key in ["pharmacy_name","geocoded_column","address"]):
#         return Pharmacy(dct["pharmacy_name"], dct["geocoded_column"], \
#             dct["address"])
#     #print(dct, "dct")
#     return dct  # this isn't working so it's returning all columns...












    # for i in filter_data.location:
    #     print(i)
    #     for key, val in i.items():
    #         if i[key] == "latitude":
    #             x = i.val


        # for lib_dict in results: 
        #     #print(lib_dict, "lib_dict")
        #     library = _decode_library_data(lib_dict)

        #     libraries.append(library)

        # return libraries # why does libs = dpc.get_libraries() return list of objects
