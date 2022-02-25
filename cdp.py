from matplotlib.style import library
from sodapy import Socrata
from library import Library
import json
import pandas as pd

def _decode_libray_data(dct):
    '''
    '''
    #First check that all required attributes are inside the dictionary 
    if all (key in dct for key in ["name_","location","address"]):
        return Library(dct["name_"],(dct["location"]['latitude'],dct["location"]['longitude']) ,dct["address"])
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
        #print(results, "results")
        for lib_dict in results: 
            library = _decode_libray_data(lib_dict)
            libraries.append(library)

        return libraries

    def find_pharmacies(self):
        '''
        '''
        pharmacies = [] 
        results = self.client.get("2et2-5aw3")

        for pharm_dict in results: 
            pharmacy = _decode_libray_data(pharm_dict)
            pharmacies.append(pharmacy)

        return pharmacies



# Converting to pandas dataframe 
# in different file?
def obj_dict(self, obj):
    '''
    '''
    return obj.__dict__


def to_json_libraries(obj_dict):
    '''
    '''
    dpc = DataPortalCollector()
    libs = dpc.find_libraries(100)
    # convert list to json
    json_string = json.dumps(libs, default = obj_dict)

    return json_string


def to_pandas(obj_dict):
    '''
    '''
    json_string = to_json_libraries(obj_dict)
    libraries_pd = pd.read_json(json_string)
    return libraries_pd


# li = cdp.to_pandas(json_string, obj_dict)













# json_string = json.dumps(list_name, default=obj_dict)
# # loading in ipython3 # 

# dpc = DataPortalCollector()
# libs = dpc.find_libraries(100)

# for lib in libs:
#     print(type(print(lib)))


# # how to call this:
# ipython libviewer.py -- --limit=1000

# view things in dataframe
#li.columns
# li.loc[:,"name"]
#li.loc[:,"coordinates"]