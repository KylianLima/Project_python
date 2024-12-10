import pygame
import random
import math

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
    
    def __init__(self, x, y, points_de_vie, attaque, defense, couleur, forme, equipe, nom):
        self.x = x
        self.y = y
        self.points_de_vie = points_de_vie
        self.attaque = attaque
        self.defense = defense
        #self.vitesse = vitesse
        self.couleur = couleur
        self.forme = forme  # "triangle", "cercle", "losange"
        self.equipe = equipe  # "Equipe 1" ou "Equipe 2"
        self.u_active = False
        self.nom = nom
        self.portee = 2
        

    def deplacement(self, dx, dy):
        #print(f"{self.nom} se déplace vers {direction}.")
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx <= LARGEUR//GRILLE_TAILLE-1 and 0 <= self.y + dy <= HAUTEUR//GRILLE_TAILLE-1:
            self.x += dx
            self.y += dy
        #Probleme: sort de la fenetre => Résolu
    
    def attaquer(self, cible):
        # #print(f"{self.nom} attaque {cible.nom} avec {self.attaque} points de puissance.")
        # dommages = max(0, self.attaque - cible.defense)
        # cible.points_de_vie -= dommages
        # #print(f"{cible.nom} subit {dommages} dégâts. PV restants : {cible.points_de_vie}")
        
        """Attaque une unité cible si elle est dans la portée."""
        distance = math.sqrt((self.x - cible.x) ** 2 + (self.y - cible.y) ** 2)
        if distance <= self.portee:  # Vérifie si la cible est à portée
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
            pygame.draw.polygon(fenetre, self.couleur, points)
        elif self.forme == "cercle": #Sorcier
            pygame.draw.circle(fenetre, self.couleur, (centre_x, centre_y), GRILLE_TAILLE // 3)
        elif self.forme == "losange": #Barbare
            points = [
                (centre_x, centre_y - GRILLE_TAILLE // 3),  # Haut
                (centre_x - GRILLE_TAILLE // 3, centre_y),  # Gauche
                (centre_x, centre_y + GRILLE_TAILLE // 3),  # Bas
                (centre_x + GRILLE_TAILLE // 3, centre_y),  # Droite
            ]
            pygame.draw.polygon(fenetre, self.couleur, points)
            
        # Afficher le nom et les points de vie
        font = pygame.font.SysFont(None, 20)
        nom_texte = font.render(f"{self.nom}", True, GRIS)
        pv_texte = font.render(f"PV: {self.points_de_vie}", True, GRIS)
        fenetre.blit(nom_texte, (case_x, case_y - 15))  # Nom au-dessus de l'unité
        fenetre.blit(pv_texte, (case_x, case_y + GRILLE_TAILLE))  # PV en dessous de l'unité
