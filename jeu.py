import pygame
import random

# Paramètres de la fenêtre
LARGEUR, HAUTEUR = 800, 600 
GRILLE_TAILLE = 40  # Taille d'une case
#20 cases en longueur et 15 en hauteur

# Couleurs
GRIS = (200, 200, 200)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)  # Eau
ROUGE = (255, 0, 0)  # Lave
BLANC = (255, 255, 255)  # VIe

"""cases de départ des unités -joueur1- (0,0) , (0,1) , (0,2) -joueur 2- (19,14) , (18,14) , (17,14)
Eviter ces cases la pour generation des cases aleatoires +1 pour espace
"""
cases_evitables = [(0,0) , (1,0) , (2,0) ,(19,14) , (18,14) , (17,14)]

class Game:
    """
    Classe pour représenter le jeu.
    """

    def __init__(self, fenetre):
        """
        Construit le jeu avec la surface de la fenêtre.
        """
        self.fenetre = fenetre
        self.cases_speciales = self.generer_cases_speciales()

    def generer_cases_speciales(self):
        """
        Génère des cases spéciales avec des couleurs spécifiques aléatoirement.

        Retourne
        --------
        dict
            Un dictionnaire où les clés sont des tuples (x, y) représentant les coordonnées
            et les valeurs sont des couleurs représentant le type de case spéciale.
        """
        cases = {}
        for _ in range(25):  # 25 cases d'eau
            x, y = random.randint(0, (LARGEUR // GRILLE_TAILLE )- 1), random.randint(0,( HAUTEUR // GRILLE_TAILLE )- 1)
            if (x,y) not in cases_evitables:
                cases[(x, y)] = BLEU
            #Avoir la compétence savoir nager pour passer à travers
        for _ in range(15):  # 15 cases de lave
            x, y = random.randint(0, (LARGEUR // GRILLE_TAILLE) - 1), random.randint(0, (HAUTEUR // GRILLE_TAILLE) - 1)
            if (x,y) not in cases_evitables:
                cases[(x, y)] = ROUGE
            #Tue n'importe quel unité sauf sorcier qui annule
        for _ in range(6):  # 6 cases de pouvoir spécial
            x, y = random.randint(0, (LARGEUR // GRILLE_TAILLE) - 1), random.randint(0, (HAUTEUR // GRILLE_TAILLE )- 1)
            if (x,y) not in cases_evitables:
                cases[(x, y)] = BLANC
            #Redonne tous les points de vie
        return cases

    def dessiner_grille(self):
        """Dessine une grille sur l'écran avec des cases spéciales."""
        self.fenetre.fill(NOIR)
        for x in range(0, LARGEUR, GRILLE_TAILLE):
            for y in range(0, HAUTEUR, GRILLE_TAILLE):
                rect = pygame.Rect(x, y, GRILLE_TAILLE, GRILLE_TAILLE)
                coord = (x // GRILLE_TAILLE, y // GRILLE_TAILLE)
                if coord in self.cases_speciales:
                    pygame.draw.rect(self.fenetre, self.cases_speciales[coord], rect)
                pygame.draw.rect(self.fenetre, GRIS, rect, 1)  # Bordures de la grille


def main():
    # Initialisation de Pygame
    pygame.init()

    # Fenêtre
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Grille de jeu avec cases spéciales")

    # Instanciation du jeu
    game = Game(fenetre)
    print(game.cases_speciales)
    # Boucle principale du jeu
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

        game.dessiner_grille()  # Dessiner la grille avec cases spéciales
        pygame.display.update()  # Mettre à jour l'affichage

    pygame.quit()


if __name__ == "__main__":
    main()
