'''
Import demographic data as pandas dataframes
Demographics includes columns related to race and population.
Income includes columns for poverty and annual income levels.
'''

import pandas as pd


# four missing per capita income
# 3 missing demographics

def import_demographics():
    '''
    '''
    
    demographics = pd.read_csv("data/Census2020SupplementCCA.csv")
    demographics = demographics.iloc[:,[1,2,6,7,8,9]]
    
    racial_columns = ["WHITE","BLACK","ASIAN","OTHER"]
    replace_values = {"The Loop" : "Loop", "O'Hare": "Ohare", "McKinley Park" : "Mckinley Park"} 

    dem_percents = demographics.copy()

    for column in racial_columns:
        dem_percents["share" + "_" + column] = dem_percents[column]/dem_percents["TOT_POP"]
    
    dem_percents = dem_percents.rename(columns = {"GEOG": "neighbor"})
    dem_percents = dem_percents.replace({"neighbor" : replace_values})

    return dem_percents

    # loop 31
    # mckliney park 58
    # oahre 75

def import_income():
    '''
    '''    
    income = pd.read_csv("data/income.csv")
    income = income.iloc[:-1 , :]
    income = income[["COMMUNITY AREA NAME", "PER CAPITA INCOME ", "HARDSHIP INDEX"]]

    replace_values = {"Montclaire" : "Montclare", "Humboldt park" : "Humboldt Park", \
        "McKinley Park" : "Mckinley Park", "Washington Height" : "Washington Heights"} 

    income = income.rename(columns = {"PER CAPITA INCOME ": "PER CAPITA INCOME"})
    income["income_per_1000"] = income["PER CAPITA INCOME"]/1000
    income = income.rename(columns = {"COMMUNITY AREA NAME": "neighbor"})
    income = income.replace({"neighbor" : replace_values})

    # Montclaire = 17
    # Humboldt park22
    # McKinley Park 58
    # Washington Height 72

    return income


def combine_dataframes():
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
    demographics = import_demographics()
    income = import_income()
    dem_stats = (demographics, income)
    return dem_stats


# demographics = ("data/Census2020SupplementCCA.csv")
# income = "income.csv"

# def dem_dataframes(income):
#     '''
#     Import two csvs into pandas dataframes.
#     One csv includes data on population and 
#         racial characteristics of neighborhoods
#         in Chicago. The other has data on income 
#         and poverty indicators for neighborhoods.
#     Inputs:
#         - none
#     Returns:
#         - dem_stats (tuple): tuple of two dataframes
#     '''
#     income = pd.read_csv("income")
#     income = income.iloc[:-1 , :]
#     dem_stats = (demographics, income)
    
#     return dem_stats
