import Unite

class Archer(Unite):
    def __init__(self):
        super().__init__("Archer", points_de_vie=70, attaque=15, defense=10, vitesse=8)