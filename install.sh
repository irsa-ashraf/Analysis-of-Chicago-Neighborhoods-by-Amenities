echo -e "1. Creating new virtual environment..."

# creating virtual env 
python3 -m venv env 

echo -e "2. Installing Requirements..."

# going into the virtual env 
source env/bin/activate 

# installing packages
pip install -r requirements.txt  # pip or pip3? 

# jump out of virtual env 
deactivate 
echo -e "Install is complete"



