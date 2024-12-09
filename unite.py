import pygame
import random

# Paramètres de la fenêtre
LARGEUR, HAUTEUR = 800, 600
GRILLE_TAILLE = 40  # Taille d'une case

# Couleurs
GRIS = (200, 200, 200)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)  # Eau
ROUGE = (255, 0, 0)  # Lave
BLANC = (255, 255, 255)  # Pouvoir spécial
VERT = (0, 255, 0)  # Archer
ORANGE = (255, 165, 0)  # Sorcier
JAUNE = (255, 255, 0)  # Barbare

class Unite:
    
    def __init__(self, x, y, points_de_vie, attaque, defense, couleur, forme, equipe):
        self.x = x
        self.y = y
        self.points_de_vie = points_de_vie
        self.attaque = attaque
        self.defense = defense
        #self.vitesse = vitesse
        self.couleur = couleur
        self.forme = forme  # "triangle", "cercle", "losange"
        self.equipe = equipe  # "Equipe 1" ou "Equipe 2"

    def deplacement(self, dx, dy):
        #print(f"{self.nom} se déplace vers {direction}.")
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRILLE_TAILLE and 0 <= self.y + dy < GRILLE_TAILLE:
            self.x += dx
            self.y += dy
        
    
    def attaquer(self, cible):
        #print(f"{self.nom} attaque {cible.nom} avec {self.attaque} points de puissance.")
        dommages = max(0, self.attaque - cible.defense)
        cible.points_de_vie -= dommages
        #print(f"{cible.nom} subit {dommages} dégâts. PV restants : {cible.points_de_vie}")
    
    def dessiner(self, fenetre):
        """Dessine l'unité sur la grille."""
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
