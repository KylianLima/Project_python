import Unite

class Sorcier(Unite):
    def __init__(self):
        super().__init__("Sorcier", points_de_vie=60, attaque=30, defense=5, vitesse=7)
        
    def lancer_sort(self, cible):
        #print(f"{self.nom} lance un sort sur {cible.nom}.")
        cible.points_de_vie -= 25
        #print(f"{cible.nom} subit 25 dégâts magiques. PV restants : {cible.points_de_vie}")

