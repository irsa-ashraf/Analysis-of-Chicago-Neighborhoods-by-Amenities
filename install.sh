echo -e "1. Creating new virtual environment..."

# deleting old one if it already exists 
if [[ -d env ]]; then
    echo -e "\t--Virtual Environemnt already exists. Deleting old one now."
    rm -rf env
fi

# creating virtual env 
python3 -m venv env 

# not sure if following code (12-16) is necessary?
if [[ ! -d env ]]; then
    echo -e "\t--Could not create virtial environment...Please make sure venv is installed"
    exit 1
fi

echo -e "2. Installing Requirements..."

# going into the virtual env 
source env/bin/activate 

# installing packages
pip install -r requirements.txt  # pip or pip3? 

# check if we need to install additonal libraries 

# jump out of virtual env 
deactivate 
echo -e "Install is complete"

# hash -r (do we need to use this too?)

