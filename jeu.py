import pygame
import random
from unite import*

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
        self.unites = self.creer_unites()
        self.unite_active_index = 0
        self.joueur_actuel = "Equipe 1"

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
                
                
    def creer_unites(self):
        """Crée deux équipes d'unités."""
        equipe_1 = [
            Unite(0, 0, 100 , 10,30,JAUNE, "triangle", "Equipe 1"),  # Archer
            Unite(1, 0, 100 , 10,30,JAUNE, "cercle", "Equipe 1"),  # Sorcier
            Unite(2, 0, 100 , 10,30,JAUNE, "losange", "Equipe 1"),  # Barbare
        ]
        equipe_2 = [
            Unite(19, 14, 100 , 10,30,ORANGE, "triangle", "Equipe 2"),  # Archer
            Unite(18, 14, 100 , 10,30,ORANGE, "cercle", "Equipe 2"),  # Sorcier
            Unite(17, 14, 100 , 10,30,ORANGE, "losange", "Equipe 2"),  # Barbare
        ]
        return equipe_1 + equipe_2
    
    def dessiner_unites(self):
        """Dessine toutes les unités."""
        # unites_joueur = [u for u in self.unites if u.equipe == self.joueur_actuel]
        # for i, unite in enumerate(unites_joueur):
        #     u_active = (i == self.unite_active_index)
        #     unite.dessiner(self.fenetre, u_active)
        
        for unite in self.unites:
            unite.dessiner(self.fenetre)
            
    def gerer_touches(self, event):
        """Gère les touches en fonction de l'événement `KEYDOWN`."""
        unites_joueur = [u for u in self.unites if u.equipe == self.joueur_actuel]
        unite_active = unites_joueur[self.unite_active_index]
        unite_active.u_active = True

        if event.key == pygame.K_UP:
            unite_active.deplacement(0,-1)
        elif event.key == pygame.K_DOWN:
            unite_active.deplacement(0,1)
        elif event.key == pygame.K_LEFT:
            unite_active.deplacement(-1,0)
        elif event.key == pygame.K_RIGHT:
            unite_active.deplacement(1,0)
        elif event.key == pygame.K_TAB:
            self.unite_active_index = (self.unite_active_index + 1) % len(unites_joueur)
            unite_active.u_active = False
        elif event.key == pygame.K_SPACE:
            self.joueur_actuel = "Equipe 2" if self.joueur_actuel == "Equipe 1" else "Equipe 1"
            self.unite_active_index = 0
            unite_active.u_active = False
            


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
            elif event.type == pygame.KEYDOWN:
                game.gerer_touches(event)  # Gérer les appuis de touches

        game.dessiner_grille() # Dessiner la grille avec cases spéciales
        game.dessiner_unites()
        pygame.display.update()  # Mettre à jour l'affichage

    pygame.quit()


if __name__ == "__main__":
    main()
