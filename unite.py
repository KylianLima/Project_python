import pygame
import random
import math
from jeu import*

# Paramètres de la fenêtre
LARGEUR, HAUTEUR = 800, 600
GRILLE_TAILLE = 40  # Taille d'une case

# Couleurs
GRIS = (200, 200, 200)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)  # Eau
ROUGE = (255, 0, 0)  # Lave
BLANC = (255, 255, 255)  # Pouvoir spécial
VERT = (0, 255, 0)  # Selection
ORANGE = (255, 165, 0)  # Equipe 2
JAUNE = (255, 255, 0)  # Equipe 1

class Unite:
    
    def __init__(self, x, y, points_de_vie, attaque, defense, vitesse, couleur, forme, equipe, nom):
        self.x = x
        self.y = y
        self.points_de_vie = points_de_vie
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.couleur = couleur
        self.forme = forme  # "triangle", "cercle", "losange"
        self.equipe = equipe  # "Equipe 1" ou "Equipe 2"
        self.u_active = False
        self.nom = nom
        #self.portee = self.calculer_portee()
        self.image_archer = pygame.image.load("archer.png")
        self.image_archer = pygame.transform.scale(self.image_archer, (GRILLE_TAILLE, GRILLE_TAILLE))
        self.image_barbare = pygame.image.load("barbare.png")
        self.image_barbare = pygame.transform.scale(self.image_barbare, (GRILLE_TAILLE, GRILLE_TAILLE))
        self.image_sorcier = pygame.image.load("sorcier.png")
        self.image_sorcier = pygame.transform.scale(self.image_sorcier, (GRILLE_TAILLE, GRILLE_TAILLE))

    def deplacement(self, dx, dy,cases_speciales):
        #print(f"{self.nom} se déplace vers {direction}.")
        """Déplace l'unité de dx, dy."""
        # if 0 <= self.x + dx * self.vitesse <= LARGEUR//GRILLE_TAILLE-1 and 0 <= self.y + dy *self.vitesse <= HAUTEUR//GRILLE_TAILLE-1:
        #     self.x += dx * self.vitesse
        #     self.y += dy * self.vitesse
        # #Probleme: sort de la fenetre => Résolu
        #     # Vérifier si une case spéciale existe à cette position
        #     for case in cases_speciales:
        #         if not case.x == self.x and case.y == self.y:
        #             case.interact(self,cases_speciales)
                    
        new_x = self.x + dx * self.vitesse
        new_y = self.y + dy * self.vitesse

        # Vérifier les limites
        if 0 <= new_x < LARGEUR // GRILLE_TAILLE-1 and 0 <= new_y < HAUTEUR // GRILLE_TAILLE-1:
            # Vérifier s'il y a une case spéciale à la nouvelle position
            for case in cases_speciales:
                if case.x == new_x and case.y == new_y:
                    # Si la case empêche le déplacement, arrêter
                    if not case.interact(self, cases_speciales):
                        return

        # Déplacer l'unité
        self.x = new_x
        self.y = new_y
    
    def attaquer(self, cible):
        # #print(f"{self.nom} attaque {cible.nom} avec {self.attaque} points de puissance.")
        # dommages = max(0, self.attaque - cible.defense)
        # cible.points_de_vie -= dommages
        # #print(f"{cible.nom} subit {dommages} dégâts. PV restants : {cible.points_de_vie}")
        
        """Attaque une unité cible si elle est dans la portée."""
        portee = self.calculer_portee()  # Obtenir les cases de portée d'attaque
        if (cible.x, cible.y) in portee:  # Vérifier si la cible est dans la portée
            dommages = max(0, self.attaque - ((self.attaque*cible.defense)//100))
            cible.points_de_vie -= dommages
            print(f"{self.nom} attaque {cible.nom} ! {cible.nom} subit {dommages} dégâts.")
        else:
            print(f"{cible.nom} est hors de portée !")
        
    def dessiner(self, fenetre,u_active):
        """Dessine l'unité sur la grille."""
        # Coordonnées de la case
        case_x = self.x * GRILLE_TAILLE
        case_y = self.y * GRILLE_TAILLE
        
        
        if self.equipe == "Equipe 1":
            pygame.draw.rect(fenetre, self.couleur, (case_x, case_y, GRILLE_TAILLE, GRILLE_TAILLE))
            
        elif self.equipe == "Equipe 2":
            pygame.draw.rect(fenetre, self.couleur, (case_x, case_y, GRILLE_TAILLE, GRILLE_TAILLE))
        else:
            pygame.draw.rect(fenetre, self.couleur, (case_x, case_y, GRILLE_TAILLE, GRILLE_TAILLE))

        # Dessiner un carré vert derrière si l'unité est active
        if u_active:
            pygame.draw.rect(fenetre, VERT, (case_x, case_y, GRILLE_TAILLE, GRILLE_TAILLE))
            
        
        
        
        # Coordonnées du centre de la case
        centre_x = self.x * GRILLE_TAILLE + GRILLE_TAILLE // 2
        centre_y = self.y * GRILLE_TAILLE + GRILLE_TAILLE // 2

        if self.forme == "triangle": #Archer
            points = [
                (centre_x, centre_y - GRILLE_TAILLE // 3),  # Haut
                (centre_x - GRILLE_TAILLE // 3, centre_y + GRILLE_TAILLE // 3),  # Bas gauche
                (centre_x + GRILLE_TAILLE // 3, centre_y + GRILLE_TAILLE // 3),  # Bas droite
            ]
            #pygame.draw.polygon(fenetre, self.couleur, points)
            fenetre.blit(self.image_archer, (case_x, case_y))
            
        elif self.forme == "cercle": #Sorcier
            #pygame.draw.circle(fenetre, self.couleur, (centre_x, centre_y), GRILLE_TAILLE // 3)
            fenetre.blit(self.image_sorcier, (case_x, case_y))
            
            
        elif self.forme == "losange": #Barbare
            points = [
                (centre_x, centre_y - GRILLE_TAILLE // 3),  # Haut
                (centre_x - GRILLE_TAILLE // 3, centre_y),  # Gauche
                (centre_x, centre_y + GRILLE_TAILLE // 3),  # Bas
                (centre_x + GRILLE_TAILLE // 3, centre_y),  # Droite
            ]
            #pygame.draw.polygon(fenetre, self.couleur, points)
            fenetre.blit(self.image_barbare, (case_x, case_y))

            
        # Afficher le nom et les points de vie
        font = pygame.font.SysFont(None, 20)
        nom_texte = font.render(f"{self.nom}", True, GRIS)
        pv_texte = font.render(f"PV: {self.points_de_vie}", True, GRIS)
        fenetre.blit(nom_texte, (case_x, case_y - 15))  # Nom au-dessus de l'unité
        fenetre.blit(pv_texte, (case_x, case_y + GRILLE_TAILLE))  # PV en dessous de l'unité
        
        
    def calculer_portee(self):
        """Méthode par défaut, à redéfinir dans les sous-classes."""
        return
    
    
class Barbare(Unite):
    """Classe pour l'unité Barbare."""

    def __init__(self, x, y, couleur,equipe):
        super().__init__(x, y, 200, 20, 40, 2, couleur, "losange", equipe, "Barbare")

    def calculer_portee(self):
        """Le barbare attaque toutes les cases autour de lui."""
        portee = []
        for dx in range(-1, 2):  # -1, 0, 1
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:  # Exclure la case où il se trouve
                    portee.append((self.x + dx, self.y + dy))
        return portee
    
    """Compétences de Barbare : peut aller sur toutes les cases """
    def survit_lave(self) : 
        return True
    def nage(self) :
        return True

class Sorcier(Unite):
    """Classe pour l'unité Sorcier."""

    def __init__(self, x, y, couleur , equipe):
        super().__init__(x, y, 120, 40, 25, 1, couleur, "cercle", equipe, "Sorcier")

    def calculer_portee(self):
        """Le sorcier attaque en ligne et colonne à une distance de 2."""
        portee = []
        for i in range(1, 3):  # Distance de 1 à 2 cases
            portee.extend([
                (self.x + i, self.y),  # Droite
                (self.x - i, self.y),  # Gauche
                (self.x, self.y + i),  # Bas
                (self.x, self.y - i),  # Haut
            ])
        return portee


class Archer(Unite):
    """Classe pour l'unité Archer."""

    def __init__(self, x, y,couleur, equipe):
        super().__init__(x, y, 100, 20, 20, 1, couleur, "triangle", equipe, "Archer")

    def calculer_portee(self):
        """L'archer attaque toute la ligne et toute la colonne où il se situe."""
        portee = []
        for i in range(LARGEUR // GRILLE_TAILLE):  # Toute la ligne
            portee.append((i, self.y))
        for j in range(HAUTEUR // GRILLE_TAILLE):  # Toute la colonne
            portee.append((self.x, j))
        return portee
    
    
