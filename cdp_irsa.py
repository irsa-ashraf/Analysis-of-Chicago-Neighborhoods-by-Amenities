from sodapy import Socrata
from murals import Mural
import pandas as pd
import json 

def _decode_mural_data(dct):
    '''
    '''
    #First check that all required attributes are inside the dictionary 
    if all (key in dct for key in ["artwork_title", "street_address", "latitude", "longitude"]):
        return Mural(dct["artwork_title"], dct["street_address"], dct["latitude"], dct["longitude"])
    return dct 

class DataPortalCollector: 

    def __init__(self):
        '''
        '''
        # Unauthenticated client only works with public data sets. Note 'None'
        # in place of application token, and no username or password:
        self.client = Socrata("data.cityofchicago.org", "9Qto0x2IrJoK0BwbM4NSKwpkr")
        
    def find_murals(self):
        '''
        '''
        murals_lst = [] 
        results = self.client.get("we8h-apcf")
        # print(results[0])
        # return 
        for mural_dict in results: 
            mural = _decode_mural_data(mural_dict)
            murals_lst.append(mural)

        return murals_lst


def create_df(obj):
    '''
    '''

    obj_dict = obj_dict(obj)
    df = to_pandas(obj_dict)
    # json_str = to_json_murals(obj_dict)
    return df


def obj_dict(obj):
    '''
    '''
    return obj.__dict__


def to_json_murals(obj):
    '''
    '''

    o_dict = obj_dict(obj)
    dpc = DataPortalCollector()
    murals = dpc.find_murals()
    # convert list to json
    json_string = json.dumps(murals, default = o_dict)

    return json_string


def to_pandas(obj):
    '''
    '''
    json_string = to_json_murals(obj)
    murals_df = pd.read_json(json_string)

    return murals_df