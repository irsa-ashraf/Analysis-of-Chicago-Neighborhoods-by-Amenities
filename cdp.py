from matplotlib.style import library
from sodapy import Socrata

import json
import pandas as pd

from library import Library
from pharmacy import Pharmacy

def _decode_library_data(dct):
    '''
    '''
    #First check that all required attributes are inside the dictionary 
    if all (key in dct for key in ["name_","location","address"]):
        return Library(dct["name_"], \
            (dct["location"]['latitude'], \
            dct["location"]['longitude']), \
            dct["address"])
    return dct  

def _decode_pharmacy_data(dct):
    '''
    '''
    if all (key in dct for key in ["pharmacy_name","geocoded_column","address"]):
        return Pharmacy(dct["pharmacy_name"], \
            (dct["geocoded_column"]['coordinates'][0], \
            dct["geocoded_column"]['coordinates'][1]), \
            dct["address"])
    print(dct, "dct")
    return dct  

class DataPortalCollector: 

    def __init__(self):
        '''
        '''
        # Unauthenticated client only works with public data sets. Note 'None'
        # in place of application token, and no username or password:
        self.client = Socrata("data.cityofchicago.org", "9Qto0x2IrJoK0BwbM4NSKwpkr")
        
    def find_libraries(self):
        '''
        '''
        libraries = [] 
        results = self.client.get("x8fc-8rcq")
        print(results, "results")
        for lib_dict in results: 
            #print(lib_dict, "lib_dict")
            library = _decode_library_data(lib_dict)
            libraries.append(library)

        return libraries # why does libs = dpc.find_libraries() return list of objects

    def find_pharmacies(self):
        '''
        '''
        pharmacies = [] 
        results = self.client.get("2et2-5aw3")

        for pharm_dict in results: 
            #print(pharm_dict, "pharm_dict")
            pharmacy = _decode_pharmacy_data(pharm_dict)
            pharmacies.append(pharmacy)

        return pharmacies # but  pharms = dpc.find_pharmacies() returns something else



# Converting to pandas dataframe 
# put these functions in different file?
# also combine to call function within function so we can make these generalized to pulling anyh
# of the three datasets and then create them all in one overall function? 
# would have to review how to call function in function

def obj_dict(self, obj):
    '''
    '''
    return obj.__dict__


def to_json_libraries(obj_dict):
    '''
    '''
    dpc = DataPortalCollector()
    libs = dpc.find_libraries()
    # convert list to json
    json_string = json.dumps(libs, default = obj_dict)

    return json_string

def to_json_pharmacies(obj_dict):
    '''
    '''
    dpc = DataPortalCollector()
    libs = dpc.find_pharmacies()
    # convert list to json
    json_string = json.dumps(libs, default = obj_dict)
    #print(json_string, "json_string")

    return json_string

def to_pandas_libraries(obj_dict):
    '''
    '''
    json_string = to_json_libraries(obj_dict)
    libraries_pd = pd.read_json(json_string)
    return libraries_pd

def to_pandas_pharmacies(obj_dict):
    '''
    '''
    json_string = to_json_pharmacies(obj_dict)
    pharmacies_pd = pd.read_json(json_string)
    return pharmacies_pd

# li = cdp.to_pandas(json_string, obj_dict)


# questions for ian - do we want to split coordinates into two columns,
# one for longitude/one for latitude? Currently some of these data frames do
# coordinates column = ("longitude, latitude") and others do ("latitude", "longitude")










# json_string = json.dumps(list_name, default=obj_dict)
# # loading in ipython3 # 

# dpc = DataPortalCollector()
# libs = dpc.find_libraries()

# for lib in libs:
#     print(type(print(lib)))


# # how to call this:
# ipython libviewer.py -- --limit=1000

# view things in dataframe
#li.columns
# li.loc[:,"name"]
#li.loc[:,"coordinates"]