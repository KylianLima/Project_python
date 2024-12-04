class Unite:
    
    def __init__(self, nom, points_de_vie, attaque, defense, vitesse):
        self.nom = nom
        self.points_de_vie = points_de_vie
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse

    def deplacement(self, direction):
        #print(f"{self.nom} se déplace vers {direction}.")
        pass
    
    def attaquer(self, cible):
        #print(f"{self.nom} attaque {cible.nom} avec {self.attaque} points de puissance.")
        dommages = max(0, self.attaque - cible.defense)
        cible.points_de_vie -= dommages
        #print(f"{cible.nom} subit {dommages} dégâts. PV restants : {cible.points_de_vie}")
        