import pygame

# Couleurs
BLEU = (0, 0, 255)  # Eau
ROUGE = (255, 0, 0)  # Lave
BLANC = (255, 255, 255)  # VIe


class Case :
    """Classe qui définit les différentes cases dessinées et présentes sur la grille de jeu."""
    def __init__(self,x,y,couleur): 
        """Initialisation de la classe Case"""
        self.x = x #Coordonnées de la case
        self.y = y
        self.couleur = couleur
    
    def interact(self, unite, cases_speciales):
        """Méthode d'interaction des cases avec les différentes unités"""
        pass
    
    def dessiner_case(self, fenetre, taille):
        """Méthode pour dessiner les cases selon les paramètres données par fenetre et taille"""
        pygame.draw.rect(fenetre, self.couleur, (self.x * taille, self.y * taille, taille, taille))

    
    
class Lave(Case):
    def __init__(self , x,y):
        super().__init__(x, y, ROUGE) # Lave caractérisée par la couleur rouge
    
    def interact(self, unite, cases_speciales):
        """Si l'unité qui traverse cette case n'a pas l'attribut survit_lave(), elle meurt"""
        
        if not hasattr(unite, "survit_lave") or not unite.survit_lave():
            unite.points_de_vie = 0 # Mort de l'unité
            print(f"{unite.nom} de l'{unite.equipe} est tuée par la lave !") # Affichage dans le terminal
            return False
        else :
            return True
    
class Eau(Case):
    def __init__(self,x,y):
        super().__init__(x, y, BLEU) # Eau caractérisée par la couleur bleu 
        
    def interact(self, unite, cases_speciales):
        """Si l'unité qui tente de la traversée n'a pas l'attribut nage(), elle est bloquée"""
        
        if not hasattr(unite, "nage") or not unite.nage():
            print(f"{unite.nom} de l'{unite.equipe} ne peut pas traverser l'eau.") # Affichage dans le terminal
            return False  # Bloque le déplacement
        else : 
            return True #Laisse passer ou pénétrer

class Vie(Case):
    def __init__(self,x,y):
        super().__init__(x, y, BLANC) # Vie caractérisée par la couleur blanc
        
    def interact(self, unite, cases_speciales):
        """Cette case redonne 50 points de vie à toute unité qui s'arrête dessus, puis la case disparaît"""
        
        print(f"{unite.nom} de l'{unite.equipe} regagne 50 PV !") # Affichage terminal
        unite.points_de_vie += 50 # Mise à jour des pv de l'unité dessus
        cases_speciales.remove(self) # Disparition de la case = usage unique
        return True

