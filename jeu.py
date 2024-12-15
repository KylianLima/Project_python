import pygame
import random
from unite import*
from case import*

# Paramètres de la fenêtre
LARGEUR, HAUTEUR = 800, 600 
GRILLE_TAILLE = 40  # Taille d'une case
#20 cases en longueur et 15 en hauteur

# Couleurs
GRIS = (200, 200, 200)
COULEUR_PORTEE = (100,100,100) # Gris plus clair pour afficher la portée d'attaque
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
        self.cases_speciales = self.generer_cases_speciales() # Liste des cases spéciales
        self.unites = self.creer_unites() # Liste des unités
        self.unite_active_index = 0 # indique quelle unité est active dans la liste des unités
        self.joueur_actuel = "Equipe 1" # Le joueur qui joue, on commence par le joueur 1
        self.actions = 0 # Nombre d'actions effectuées
        self.afficher_portee = False  # Par défaut, la portée n'est pas affichée
        
        

    def generer_cases_speciales(self):
        """
        Méthode pour générer aléatoirement dans la grille, les cases spéciales du jeu.

        """
        cases = [] 
        for _ in range(25):  # 25 cases d'eau
        #On définit au hasard des coordonnées pour les cases
            x, y = random.randint(0, (LARGEUR // GRILLE_TAILLE )- 1), random.randint(0,( HAUTEUR // GRILLE_TAILLE )- 1)
            if (x,y) not in cases_evitables: # On vérifie qu'elles ne sont pas générées à l'emplacement de départ des unités
                cases.append(Eau(x,y)) # On ajoute les cases Eau avec les coordonnées aléatoires à la liste
            #Avoir la compétence savoir nager pour passer à travers
            
        # DE LA MEME MANIERE POUR LES CASES LAVE ET VIE    
        for _ in range(15):  # 15 cases de lave
            x, y = random.randint(0, (LARGEUR // GRILLE_TAILLE) - 1), random.randint(0, (HAUTEUR // GRILLE_TAILLE) - 1)
            if (x,y) not in cases_evitables:
                cases.append(Lave(x,y))
            #Tue n'importe quel unité sauf sorcier qui annule
        for _ in range(6):  # 6 cases de Vie
            x, y = random.randint(0, (LARGEUR // GRILLE_TAILLE) - 1), random.randint(0, (HAUTEUR // GRILLE_TAILLE )- 1)
            if (x,y) not in cases_evitables:
                cases.append(Vie(x,y))
            #Donne 50 PV
        return cases
    
    def verifier_unites(self):
        """Vérifie les unités et détermine si une équipe a gagné.
        Affiche le message de fin de jeu aveec l'équipe gagnante."""
        # Supprimer les unités avec PV <= 0
        self.unites = [u for u in self.unites if u.points_de_vie > 0]
        #La liste des unités n'est composée que d'unités avec des pv sup à 0

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
        
        # Liste des unités du joueur dont c'est le tour et détermine unité active
        unites_joueur = [u for u in self.unites if u.equipe == self.joueur_actuel]
        unite_active = unites_joueur[self.unite_active_index]


        # Dessiner les cases de portée
        if self.afficher_portee:
            for x, y in unite_active.calculer_portee():
                if 0 <= x < LARGEUR // GRILLE_TAILLE and 0 <= y < HAUTEUR // GRILLE_TAILLE:
                    pygame.draw.rect(self.fenetre, COULEUR_PORTEE, 
                                (x * GRILLE_TAILLE, y * GRILLE_TAILLE, GRILLE_TAILLE, GRILLE_TAILLE))
        # On dessine des cases gris clair pour représenter la portée d'attaque

        # Dessiner les cases spéciales
        for case in self.cases_speciales:
            case.dessiner_case(self.fenetre, GRILLE_TAILLE)
        
        # Dessiner la grille grise
        for x in range(0, LARGEUR, GRILLE_TAILLE):
            for y in range(0, HAUTEUR, GRILLE_TAILLE):
                rect = pygame.Rect(x, y, GRILLE_TAILLE, GRILLE_TAILLE)
                pygame.draw.rect(self.fenetre, GRIS, rect, 1)  # Bordures de la grille
                
                
    def creer_unites(self):
        """Crée deux équipes d'unités.
        L'équipe 1 est positionnée en haut à gauche de la grille.
        L'équipe 2 est positionnée en bas à droite de la grille."""
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
        return equipe_1 + equipe_2 # Liste comprenant les deux équipes
    
    def dessiner_unites(self):
        """Dessine toutes les unités."""
        
        for unite in self.unites:
           u_active = False
           if unite.equipe == self.joueur_actuel:
               unites_joueur = [u for u in self.unites if u.equipe == self.joueur_actuel]
               u_active = (unites_joueur.index(unite) == self.unite_active_index)
           unite.dessiner(self.fenetre, u_active) #Appel de la méthode dessiner() de la classe Unite
        
           
    def changer_tour(self):
        """Passe au joueur suivant et réinitialise les actions."""
        self.joueur_actuel = "Equipe 2" if self.joueur_actuel == "Equipe 1" else "Equipe 1"
        self.unite_active_index = 0
        self.actions= 0  # Réinitialiser les actions
            
    def gerer_touches(self, event):
        """Gère les touches en fonction de l'événement `KEYDOWN`."""
        
        if self.actions > 4:
            # Si 5 actions ont été effectuées,on doit appuyer sur Espace pour changer de joueur
            if event.key == pygame.K_SPACE:    
                self.changer_tour()
            else : 
                print("Aucune action restante pour ce tour ! Appuyer sur ESPACE pour passer au joueur suivant.")
            return
        
        unites_joueur = [u for u in self.unites if u.equipe == self.joueur_actuel] # Liste des unités du joueur du tour pour savoir sur lesquelles agir
        unite_active = unites_joueur[self.unite_active_index]
        unite_active.u_active = True # True pour affichage de l'unité sélectionnée
        
        #incrementation de self.actions pour limiter le nombre d'actions
        #Gestion des touches directionnelles pour déplacement des unités
        if event.key == pygame.K_UP: #Si appui haut, déplacement vers le haut
            unite_active.deplacement(0,-1,self.cases_speciales) # appel méthode déplacement de unité
            self.actions +=1
        elif event.key == pygame.K_DOWN:
            unite_active.deplacement(0,1,self.cases_speciales)
            self.actions +=1
        elif event.key == pygame.K_LEFT:
            unite_active.deplacement(-1,0,self.cases_speciales)
            self.actions +=1
        elif event.key == pygame.K_RIGHT:
            unite_active.deplacement(1,0,self.cases_speciales)
            self.actions +=1
        #TAB pour changer d'unités à controler sans compter d'action
        elif event.key == pygame.K_TAB:
            self.unite_active_index = (self.unite_active_index + 1) % len(unites_joueur)
            unite_active.u_active = False
            
        elif event.key == pygame.K_a:  # Touche pour attaquer
            if not self.afficher_portee:
                self.afficher_portee = True  # Active l'affichage de la portée
            else:
                self.afficher_portee = False  # Désactive la portée et effectue l'attaque
                self.attaquer_adverse(unite_active) # Appel de la méthode d'attaque de la classe Unite dans la méthode attaquer_adverse
                self.actions = 5 #Une seule attaque possible et fin du tour
                
        elif event.key == pygame.K_z:  # Touche pour utiliser une compétence
            self.utiliser_competence(unite_active) 
            self.actions = 5 #Une utilisation de compétence possible et fin du tour
            
        # Vérification des unités restantes après chaque action
        if self.verifier_unites():
            return


    def attaquer_adverse(self, unite_active):
        #Permet à l'unité active d'attaquer une cible adverse si elle est dans sa portée.
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
        print("Aucun adversaire à portée.") #Affichage terminal si aucune cible à portée
            
    def afficher_message(self, message):
        """Affiche un message au centre de l'écran."""
        font = pygame.font.SysFont(None, 50)
        texte = font.render(message, True, (255, 255, 255))
        texte_rect = texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
        self.fenetre.blit(texte, texte_rect)
        pygame.display.update()
        pygame.time.wait(3000)  # Attends 3 secondes avant de quitter
        pygame.quit() # Quitte le jeu
        exit() # Quitte le code
        
    def dessiner_interface(self):
        """Dessine le compteur d'actions en haut de l'écran."""
        n_actions = 5-self.actions # Décompte du nombre d'actions
        font = pygame.font.SysFont(None, 30)
        texte = font.render(f"Tour {self.joueur_actuel} actions restantes : {n_actions}", True, (255, 255, 255))
        self.fenetre.blit(texte, (10, 10))

    def utiliser_competence(self, unite_active):
        """Permet à l'unité active d'utiliser sa compétence"""
        unite_active.competence(self) # Appel de la méthode compétence de la classe Unite


def main():
    # Initialisation de Pygame
    pygame.init()

    # Fenêtre
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Grille de jeu")

    # Instanciation du jeu
    game = Game(fenetre)

    # Boucle principale du jeu
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN:
                game.gerer_touches(event)  # Gérer les appuis de touches

        game.dessiner_grille() # Dessiner la grille avec cases spéciales
        game.dessiner_unites() # Dessiner les unités
        game.dessiner_interface() # Afficher l'interface : le compteur d'actions
        pygame.display.update() # Mettre à jour l'affichage
        

    pygame.quit()


if __name__ == "__main__":
    main()
