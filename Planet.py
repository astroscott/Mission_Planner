from jplephem.spk import SPK
kernel = SPK.open('de440s.bsp')

class Planet:
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
            "num" : self.options[body]
        }


    def getCoords(self, juldates):      
        r, v = kernel[0,self.properties["num"]].compute_and_differentiate(juldates)
        return r, v/86400