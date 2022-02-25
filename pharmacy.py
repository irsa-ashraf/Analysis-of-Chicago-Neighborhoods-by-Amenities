class Pharmacy:

    def __init__(self, name, coordinates, address):
        self.name = name 
        self.coordinates = coordinates 
        self.address = address 

    def __str__(self):
        return f"Name={self.name}\nAddress={self.address}\nLocation\n\tLatitude={self.coordinates[0]}\n\tLongitude={self.coordinates[1]}"
