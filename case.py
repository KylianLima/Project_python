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
    
    def interact(self, unite, cases_speciales):
        pass
    
    def dessiner_case(self, fenetre, taille):
        pygame.draw.rect(fenetre, self.couleur, (self.x * taille, self.y * taille, taille, taille))

    
    
class Lave(Case):
    def __init__(self , x,y):
        super().__init__(x, y, ROUGE)  
    
    def interact(self, unite, cases_speciales):
        
        if not hasattr(unite, "survit_lave"):
            unite.points_de_vie = 0
            print(f"{unite.nom} de l'{unite.equipe} est tuée par la lave !")

    
class Eau(Case):
    def __init__(self,x,y):
        super().__init__(x, y, BLEU) 
        
    def interact(self, unite, cases_speciales):
        if not hasattr(unite, "nage") or not unite.nage():
            print(f"{unite.nom} de l'{unite.equipe} ne peut pas traverser l'eau.")
            return False  # Bloque le déplacement
        else : 
            return True

class Vie(Case):
    def __init__(self,x,y):
        super().__init__(x, y, BLANC) 
        
    def interact(self, unite, cases_speciales):
        print(f"{unite.nom} de l'{unite.equipe} regagne 50 PV !")
        unite.points_de_vie += 50
        cases_speciales.remove(self)
        return True

