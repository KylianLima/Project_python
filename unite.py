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
BLANC = (255, 255, 255)  # Vie
VERT = (0, 255, 0)  # Selection
ORANGE = (255, 165, 0)  # Equipe 2
JAUNE = (255, 255, 0)  # Equipe 1

class Unite:
    """ Classe des différents personnage jouables dans le jeu """
    def __init__(self, x, y, points_de_vie, attaque, defense, vitesse, couleur, equipe, nom):
        self.x = x # position de l'unité en abscisse
        self.y = y # position de l'unité en ordonnée
        self.points_de_vie = points_de_vie 
        self.attaque = attaque 
        self.defense = defense 
        self.vitesse = vitesse # la vitesse définit de combien de case l'unité se déplace
        self.couleur = couleur # Couleur de l'équipe
        self.equipe = equipe  # "Equipe 1" ou "Equipe 2"
        self.u_active = False # l'unité est celle sélectionnée ou non
        self.nom = nom 
        # Chargement des images des différentes unités de jeu
        self.image_archer = pygame.image.load("archer.png")
        self.image_archer = pygame.transform.scale(self.image_archer, (GRILLE_TAILLE, GRILLE_TAILLE))
        self.image_barbare = pygame.image.load("barbare.png")
        self.image_barbare = pygame.transform.scale(self.image_barbare, (GRILLE_TAILLE, GRILLE_TAILLE))
        self.image_sorcier = pygame.image.load("sorcier.png")
        self.image_sorcier = pygame.transform.scale(self.image_sorcier, (GRILLE_TAILLE, GRILLE_TAILLE))

    def deplacement(self, dx, dy,cases_speciales):
        """Méthode de déplacement de l'unité de dx, dy. 
        On ajoute cases spéciales pour les intéractions possibles"""
        
        #On définit une nouvelle position pour l'unité
        new_x = self.x + dx * self.vitesse 
        new_y = self.y + dy * self.vitesse
        
        # Vérifier les limites de la grille
        if 0 <= new_x < LARGEUR // GRILLE_TAILLE and 0 <= new_y < HAUTEUR // GRILLE_TAILLE :
            # Vérifier s'il y a une case spéciale à la nouvelle position
            for case in cases_speciales:
                if case.x == new_x and case.y == new_y:
                    # Si la case empêche le déplacement, arrêter
                    if not case.interact(self, cases_speciales):
                        #Sinon, l'unité intéragit avec la case si il y a intéraction
                        return

        # Déplacer l'unité une fois les vérifiactions faites
        self.x = new_x
        self.y = new_y
    
    def attaquer(self, cible):
        """Méthode permettant à l'unité d'attaquer une unité cible si elle est dans la portée."""
        portee = self.calculer_portee()  # Obtenir les cases de portée d'attaque
        if (cible.x, cible.y) in portee:  # Vérifier si la cible est dans la portée
            dommages = max(0, self.attaque - ((self.attaque*cible.defense)//100)) # Calcul des dommages en fonction de l'attaque de l'unité et la défense de la cible
            cible.points_de_vie -= dommages # On retire les dommages au pv de la cible
            print(f"{self.nom} attaque {cible.nom} ! {cible.nom} subit {dommages} dégâts.") # Affichage terminal
        else:
            print(f"{cible.nom} est hors de portée !")
        
    def dessiner(self, fenetre,u_active):
        """Dessine l'unité sur la grille."""
        # Coordonnées de la case où se situe l'unité
        case_x = self.x * GRILLE_TAILLE
        case_y = self.y * GRILLE_TAILLE
        
        
        if self.equipe == "Equipe 1": #Si l'unité fait partie de l'équipe 1, son fond est jaune 
            pygame.draw.rect(fenetre, self.couleur, (case_x, case_y, GRILLE_TAILLE, GRILLE_TAILLE))
            
        elif self.equipe == "Equipe 2": #Si l'unité fait partie de l'équipe 2, son fond est orange
            pygame.draw.rect(fenetre, self.couleur, (case_x, case_y, GRILLE_TAILLE, GRILLE_TAILLE))
        else:
            pygame.draw.rect(fenetre, self.couleur, (case_x, case_y, GRILLE_TAILLE, GRILLE_TAILLE))
            
        #Couleur définie dans la création des unités


        # Dessine un carré vert derrière si l'unité est active
        if u_active:
            pygame.draw.rect(fenetre, VERT, (case_x, case_y, GRILLE_TAILLE, GRILLE_TAILLE))
            
        # Dessine les différentes unités à leur position
        if self.nom == "Archer": 
            fenetre.blit(self.image_archer, (case_x, case_y))
            
        elif self.nom == "Sorcier": 
            fenetre.blit(self.image_sorcier, (case_x, case_y))
            
        elif self.nom == "Barbare":
            fenetre.blit(self.image_barbare, (case_x, case_y))

            
        # Afficher le nom et les points de vie
        font = pygame.font.SysFont(None, 20)
        nom_texte = font.render(f"{self.nom}", True, GRIS)
        pv_texte = font.render(f"PV: {self.points_de_vie}", True, GRIS)
        fenetre.blit(nom_texte, (case_x, case_y - 15))  # Nom au-dessus de l'unité
        fenetre.blit(pv_texte, (case_x, case_y + GRILLE_TAILLE))  # PV en dessous de l'unité
        
        
        
    """Méthodes par défaut, à redéfinir dans les sous-classes."""  
    def calculer_portee(self):
        
        return
    
    def competence(self,game):
        return
    
class Barbare(Unite):
    """Classe pour l'unité Barbare."""

    def __init__(self, x, y, couleur,equipe):
        super().__init__(x, y, 200, 20, 40, 2, couleur, equipe, "Barbare")
        #On définit le barbare avec pv = 200 attaque = 20 defense = 40 et vitesse = 2

    def calculer_portee(self): # Retourne la liste des cases qui peuvent subir l'attauqe
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
    
    def competence(self,game): #utilisation de la compétence, attaque +20
        self.attaque += 20
        print(f"Le {self.nom} de {self.equipe} augmente son attaque de 20") # Affichage dans le terminal



class Sorcier(Unite):
    """Classe pour l'unité Sorcier."""
    
    def __init__(self, x, y, couleur , equipe):
        super().__init__(x, y, 120, 40, 25, 1, couleur, equipe, "Sorcier")
        # On définit le sorcier avec pv = 120 attaque = 40 defense = 25 et vitesse = 1
        
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
    
    def competence(self, game):
        """Le Sorcier détruit les cases spéciales autour de lui."""
        print(f"Le {self.nom} a détruit les cases spéciales autour de lui !")
        cases_a_detruire = [
            (self.x + dx, self.y + dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if dx != 0 or dy != 0
        ] # Définition des cases à détruire en une liste
        game.cases_speciales = [
            case for case in game.cases_speciales
            if (case.x, case.y) not in cases_a_detruire
        ] # Mise à jour des cases du jeu sans les cases détruites par le sorcier

class Archer(Unite):
    """Classe pour l'unité Archer."""

    def __init__(self, x, y,couleur, equipe):
        super().__init__(x, y, 100, 20, 20, 1, couleur, equipe, "Archer")
        #On définit l'archer avec pv = 100 attaque = 20 defense = 20 et vitesse = 1

    def calculer_portee(self):
        """L'archer attaque toute la ligne et toute la colonne où il se situe."""
        portee = []
        for i in range(LARGEUR // GRILLE_TAILLE):  # Toute la ligne
            portee.append((i, self.y))
        for j in range(HAUTEUR // GRILLE_TAILLE):  # Toute la colonne
            portee.append((self.x, j))
        return portee # Retourne la liste de toutes les cases horizontales et verticales à l'archer
    
    def competence(self, game):
        """L'archer peut faire une attauqe de zone au corps à corps et attaquer toutes les unités autour de lui"""
        adversaires_touches = [] # Liste des adversaires touchés par l'attaque de zone
        for adversaire in game.unites: # On traverse la liste de toutes les unités du jeu
            # On vérifie l'équipe et la position
            if adversaire.equipe != self.equipe and (adversaire.x == self.x or adversaire.y == self.y):
                dommages = max(0, self.attaque - ((self.attaque*adversaire.defense)//100))
                adversaire.points_de_vie -= dommages
                adversaires_touches.append((adversaire.nom, dommages))
                
                if adversaire.points_de_vie <= 0: # En cas d'élimination
                    game.unites.remove(adversaire)
                    print(f"{adversaire.nom} a été éliminé par l'attaque de zone de {self.nom} !")
                    
        if adversaires_touches:
            print(f"{self.nom} a infligé des dégâts aux unités: {adversaires_touches}")
        else:
            print(f"Aucune unité adverse n'a été touchée par l'attaque de zone de {self.nom}.")
