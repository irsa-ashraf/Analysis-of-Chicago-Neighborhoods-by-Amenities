This project creates a map that shows the Shannon Index by neighborhood in Chicago.

Shannon Index source:
citation

How to run
1. Run source install.sh to cretae a virtual environment and install packages
2. Run python app.main in the command line
3. Click "Open in Browser" OR copy and paste the link to your preferred web browser to see the map
4. Type Ctrl + C to kill the dash output
5. Run deactivate to exit out of virtual environment

Front End
We're using Dash to create a map of Chicago with its neighborhoods and have toggles for the data points we're analyzing - libraries, pharmacies, murals and Starbucks. The map also displays demographic info (get exact details). An exmaple search could be filtering neighorhoods by presence of Starbucks and seeing the 
Shannon Index pop up over each neighborhood on the map. 

Backend
Our main data source is the Chicago Data Portal from where we are acessing data on libraries, pharmacies and murals via an API. We're also collecting data on Starbucks from ______ and census and demographic data from _____. After cleaning up the data from these sources into dataframes, we input them to dash which creates the map. 

Documentation file

Files names and description
README.md: this file
install.sh: shell script for creating a virtual environment and installing libraries
app.py: the main file that imports data from the opther files and runs the dash output
data: data directory
requirements.txt: text file with all required libraries to run this project 
# ADD PROJ FEEDBACK FILES? 

Population and racial data comes from: https://datahub.cmap.illinois.gov/dataset/community-data-snapshots-raw-data
(2020 Census Supplement: Chicago Community Area csv)
Still need to add documentation file from the website
Income source: https://data.cityofchicago.org/Health-Human-Services/Per-Capita-Income/r6ad-wvtk


API Key Information
- username: ksarussi@uchicago.edu
- app token: 9Qto0x2IrJoK0BwbM4NSKwpkr
- user secret token: 1ot2XflTozEBtprxtbPB-m2sN1p0d5Loj3tw 
- mapquest: BcNrdvBLg1ZFWdTWKfTBxmu48ehAXPGM