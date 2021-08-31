from jplephem.spk import SPK
kernel = SPK.open('de440s.bsp')

class Planet:
    # Instantiating a Planet object with the name of the planet ie: Earth = Planet("Earth") 
    # pulls a corresponding number from the "options" dict, which is then stored in the
    # properties dict. This number is passed to the jplephem library to access the JPL 
    # ephemeris data contained in de440s.bsp using the getCoords method below.

    options = {
        "Mercury" : 1,
        "Venus"   : 2,
        "Earth"   : 3,
        "Mars"    : 4,
        "Jupiter" : 5,
        "Saturn"  : 6,
        "Uranus"  : 7,
        "Neptune" : 8,
        "Pluto"   : 9
    }

    properties = {}

    def __init__(self, body):

        self.properties = {
            "name" : body,
            "num"  : self.options[body]
        }

    def getCoords(self, juldates):
        # Takes an array of julian dates and returns the position and velocity
        # vectors of the instantiated planet.     

        r, v = kernel[0,self.properties["num"]].compute_and_differentiate(juldates)

        return r, v/86400 # [km, km/s]