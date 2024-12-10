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
    
    def verifier_unites(self):
        """Vérifie les unités et détermine si une équipe a gagné."""
        # Supprimer les unités avec PV <= 0
        self.unites = [u for u in self.unites if u.points_de_vie > 0]

        # Vérifier si une équipe n'a plus d'unités
        equipe_1 = [u for u in self.unites if u.equipe == "Equipe 1"]
        equipe_2 = [u for u in self.unites if u.equipe == "Equipe 2"]

        if not equipe_1:  # Si l'équipe 1 n'a plus d'unités
            self.afficher_message("Equipe 2 a gagné !")
            return True
        if not equipe_2:  # Si l'équipe 2 n'a plus d'unités
            self.afficher_message("Equipe 1 a gagné !")
            return True

        return False
    
    def dessiner_grille(self):
        """Dessine une grille sur l'écran avec des cases spéciales."""
        self.fenetre.fill(NOIR)
        unites_joueur = [u for u in self.unites if u.equipe == self.joueur_actuel]
        unite_active = unites_joueur[self.unite_active_index]

        # Dessiner les cases de portée
        for x, y in unite_active.calculer_portee():
           if 0 <= x < LARGEUR // GRILLE_TAILLE and 0 <= y < HAUTEUR // GRILLE_TAILLE:
               pygame.draw.rect(self.fenetre, GRIS, 
                                (x * GRILLE_TAILLE, y * GRILLE_TAILLE, GRILLE_TAILLE, GRILLE_TAILLE))

        
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
            Archer(0, 0, ORANGE, "Equipe 1"),
            Sorcier(1, 0, ORANGE, "Equipe 1"),
            Barbare(2, 0, ORANGE,"Equipe 1"),
        ]
        equipe_2 = [
            Archer(19, 14, JAUNE,"Equipe 2"),
            Sorcier(18, 14, JAUNE, "Equipe 2"),
            Barbare(17, 14, JAUNE, "Equipe 2"),
        ]
        return equipe_1 + equipe_2
    
    def dessiner_unites(self):
        """Dessine toutes les unités."""
        # unites_joueur = [u for u in self.unites if u.equipe == self.joueur_actuel]
        # for i, unite in enumerate(unites_joueur):
        #     u_active = (i == self.unite_active_index)
        #     unite.dessiner(self.fenetre, u_active)
        
        # for unite in self.unites:
        #     unite.dessiner(self.fenetre)
        
        for unite in self.unites:
           u_active = False
           if unite.equipe == self.joueur_actuel:
               unites_joueur = [u for u in self.unites if u.equipe == self.joueur_actuel]
               u_active = (unites_joueur.index(unite) == self.unite_active_index)
           unite.dessiner(self.fenetre, u_active)
            
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
        elif event.key == pygame.K_a:  # Touche pour attaquer
            self.attaquer_adverse(unite_active)
            
        # Vérifier les unités restantes après chaque action
        if self.verifier_unites():
            return
            
            
    # def attaquer_adverse(self, unite_active):
    #     """Permet à l'unité active d'attaquer une cible adverse."""
    #     adversaires = [u for u in self.unites if u.equipe != self.joueur_actuel]
    #     for adversaire in adversaires:
    #         distance = ((unite_active.x - adversaire.x) ** 2 + (unite_active.y - adversaire.y) ** 2) ** 0.5
    #         if distance <= unite_active.portee:
    #             unite_active.attaquer(adversaire)
    #             break

    def attaquer_adverse(self, unite_active):
        """Permet à l'unité active d'attaquer une cible adverse si elle est dans sa portée."""
        adversaires = [u for u in self.unites if u.equipe != self.joueur_actuel]
        portee = unite_active.calculer_portee()

        for adversaire in adversaires:
            if (adversaire.x, adversaire.y) in portee:  # Vérifie si l'adversaire est dans la portée
                unite_active.attaquer(adversaire)

                # Supprimer l'adversaire s'il est mort
                if adversaire.points_de_vie <= 0:
                    self.unites.remove(adversaire)
                    print(f"{adversaire.nom} a été éliminé !")

                return  # Attaque terminée après avoir trouvé une cible valide
        print("Aucun adversaire à portée.")
            
    def afficher_message(self, message):
        """Affiche un message au centre de l'écran."""
        font = pygame.font.SysFont(None, 50)
        texte = font.render(message, True, (255, 255, 255))
        texte_rect = texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
        self.fenetre.blit(texte, texte_rect)
        pygame.display.update()
        pygame.time.wait(3000)  # Attendre 3 secondes avant de quitter
        pygame.quit()
        exit()


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
