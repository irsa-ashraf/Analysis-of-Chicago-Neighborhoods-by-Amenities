'''
Import demographic data as pandas dataframes
Demographics includes columns related to race and population.
Income includes columns for poverty and annual income levels.
'''

import pandas as pd

def dem_dataframes():
    '''
    Import two csvs into pandas dataframes.
    One csv includes data on population and 
        racial characteristics of neighborhoods
        in Chicago. The other has data on income 
        and poverty indicators for neighborhoods.
    Inputs:
        - none
    Returns:
        - dem_stats (tuple): tuple of two dataframes
    '''

    demographics = pd.read_csv("data/Census2020SupplementCCA.csv")
    income = pd.read_csv("data/income.csv")
    income = income.iloc[:-1 , :]
    dem_stats = (demographics, income)
    
    return dem_stats


demographics = ("data/Census2020SupplementCCA.csv")
income = "income.csv"

def dem_dataframes(income):
    '''
    Import two csvs into pandas dataframes.
    One csv includes data on population and 
        racial characteristics of neighborhoods
        in Chicago. The other has data on income 
        and poverty indicators for neighborhoods.
    Inputs:
        - none
    Returns:
        - dem_stats (tuple): tuple of two dataframes
    '''
    income = pd.read_csv("income")
    income = income.iloc[:-1 , :]
    dem_stats = (demographics, income)
    
    return dem_stats
