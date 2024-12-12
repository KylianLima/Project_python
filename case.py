from unite import*
from jeu import*
import pygame
# Couleurs
GRIS = (200, 200, 200)
COULEUR_PORTEE = (100,100,100)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)  # Eau
ROUGE = (255, 0, 0)  # Lave
BLANC = (255, 255, 255)  # VIe


class Case :
    def __init__(self,x,y,couleur): 
        self.x = x
        self.y = y
        self.couleur = couleur
    
    def interact(self, unite):
        pass
    
    def dessiner_case(self, fenetre, taille):
        pygame.draw.rect(fenetre, self.couleur, (self.x * taille, self.y * taille, taille, taille))

    
    
class Lave(Case):
    def __init__(self , x,y):
        super().__init__(x, y, ROUGE)  
    
    def interact(self, unite):
        print(f"{unite.nom} de l'{unite.equipe} est tuée par la lave !")
        unite.points_de_vie = 0

    
class Eau(Case):
    def __init__(self,x,y):
        super().__init__(x, y, BLEU) 
        
    def interact(self, unite):
        pass

class Vie(Case):
    def __init__(self,x,y):
        super().__init__(x, y, BLANC) 
        
    def interact(self, unite):
        print(f"{unite.nom} de l'{unite.equipe} regagne 50 PV !")
        unite.points_de_vie += 50

