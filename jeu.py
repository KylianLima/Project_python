import pygame
import random

# Paramètres de la fenêtre
LARGEUR, HAUTEUR = 800, 600
GRILLE_TAILLE = 40  # Taille d'une case

# Couleurs
GRIS = (200, 200, 200)
NOIR = (0, 0, 0)


class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, fenetre):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.fenetre = fenetre
        
    def dessiner_grille(self,fenetre):
        """Dessine une grille sur l'écran."""
        self.fenetre.fill(NOIR)
        for x in range(0, LARGEUR, GRILLE_TAILLE):
            for y in range(0, HAUTEUR, GRILLE_TAILLE):
                rect = pygame.Rect(x, y, GRILLE_TAILLE, GRILLE_TAILLE)
                pygame.draw.rect(self.fenetre, GRIS, rect, 1)
        pygame.display.flip()
        


def main():

    # Initialisation de Pygame
    pygame.init()

    # Fenêtre
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Grille de jeu")
    
    # Instanciation du jeu
    game = Game(fenetre)

    # Boucle principale du jeu
    while True:
        
        game.dessiner_grille(fenetre)  # Dessiner la grille

        pygame.display.update()  # Mettre à jour l'affichage

main()
pygame.quit()
