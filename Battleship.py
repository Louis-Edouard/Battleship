import tkinter as tk
from tkinter import messagebox
import random

# Classe principale de l'application Bataille Navale
class BatailleNavaleApp:
    def __init__(self, root):
        # Initialisation de la fenêtre principale
        self.root = root
        self.root.title("Bataille Navale")
        self.root.resizable(False, False)

        # États et paramètres de jeu
        self.phase_placement = True  # Indique si on est dans la phase de placement des navires
        self.tour_joueur = True  # Détermine si c'est le tour du joueur (True) ou de l'ordinateur (False)
        self.navires_a_placer = [  # Liste des navires à placer, avec leurs noms et tailles respectives
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer 1", 3),
            ("Destroyer 2", 3),
            ("Sous-marin 1", 2),
            ("Sous-marin 2", 2),
        ]
        self.orientation = "horizontal"  # Orientation des navires placés par le joueur

        # Initialisation des plateaux et des joueurs
        self.plateau_joueur = Plateau()
        self.plateau_ordinateur = Plateau()
        self.joueur = Joueur("Joueur", self.plateau_joueur)
        self.ordinateur = Joueur("Ordinateur", self.plateau_ordinateur)

        # Création de l'interface utilisateur
        self._creer_interface()

        # Placement automatique des navires pour l'ordinateur
        self._placement_automatique_ordinateur()

    # Méthode pour créer l'interface graphique
    def _creer_interface(self):
        # Plateau du joueur
        tk.Label(self.root, text="Votre Plateau").grid(row=0, column=0, pady=5)
        self.grille_joueur = self._creer_grille(self.plateau_joueur, "placement", row_offset=1, col_offset=0)

        # Plateau de l'ordinateur
        tk.Label(self.root, text="Plateau de l'Ordinateur").grid(row=0, column=1, pady=5)
        self.grille_ordinateur = self._creer_grille(self.plateau_ordinateur, "attaque", row_offset=1, col_offset=1)

        # Panneau de contrôle pour afficher des informations et des boutons d'action
        self.panneau_controle = tk.Frame(self.root)
        self.panneau_controle.grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.panneau_controle, text="Nouvelle Partie", command=self.nouvelle_partie).grid(row=0, column=0, padx=5)
        self.label_tour = tk.Label(self.panneau_controle, text="Placement des navires : Porte-avions")
        self.label_tour.grid(row=1, column=0, columnspan=2, pady=5)

    # Méthode pour créer une grille de boutons pour un plateau donné
    def _creer_grille(self, plateau, mode, row_offset, col_offset):
        grille = []
        for x in range(plateau.taille):  # Parcourt les lignes
            ligne = []
            for y in range(plateau.taille):  # Parcourt les colonnes
                bouton = tk.Button(
                    self.root,
                    width=2,
                    height=1,
                    command=lambda x=x, y=y, mode=mode: self._gerer_clic(x, y, mode)  # Associe un clic à une action
                )
                bouton.grid(row=x + row_offset, column=y + col_offset * plateau.taille, padx=1, pady=1)
                ligne.append(bouton)
            grille.append(ligne)
        return grille

    # Gestion des clics sur les boutons des grilles
    def _gerer_clic(self, x, y, mode):
        if mode == "placement" and self.phase_placement:
            self._placer_navire(x, y)
        elif mode == "attaque" and not self.phase_placement and self.tour_joueur:
            self._tir_joueur(x, y)

    # Placement d'un navire sur le plateau du joueur
    def _placer_navire(self, x, y):
        if self.navires_a_placer:  # Si des navires restent à placer
            nom, taille = self.navires_a_placer[0]
            navire = Navire(nom, taille)
            if self.plateau_joueur.placer_navire(navire, (x, y), self.orientation):
                self._mettre_a_jour_grille(self.grille_joueur, self.plateau_joueur)
                self.navires_a_placer.pop(0)  # Retirer le navire placé de la liste
                if self.navires_a_placer:
                    self.label_tour.config(text=f"Placement des navires : {self.navires_a_placer[0][0]}")
                else:
                    self.phase_placement = False
                    self.label_tour.config(text="À vous de jouer !")

    # Placement automatique des navires pour l'ordinateur
    def _placement_automatique_ordinateur(self):
        for nom, taille in self.navires_a_placer:
            navire = Navire(nom, taille)
            place = False
            while not place:  # Essayer jusqu'à réussir à placer un navire
                x, y = random.randint(0, 9), random.randint(0, 9)
                orientation = random.choice(["horizontal", "vertical"])
                place = self.plateau_ordinateur.placer_navire(navire, (x, y), orientation)

    # Mise à jour de l'affichage de la grille
    def _mettre_a_jour_grille(self, grille, plateau):
        for x in range(plateau.taille):
            for y in range(plateau.taille):
                if plateau.grille[x][y] == "O":
                    grille[x][y].config(bg="gray")  # Indique la présence d'un navire

    # Gestion d'un tir du joueur sur le plateau de l'ordinateur
    def _tir_joueur(self, x, y):
        if self.plateau_ordinateur.tirer((x, y)):  # Si le tir touche
            self.grille_ordinateur[x][y].config(bg="red")
        else:
            self.grille_ordinateur[x][y].config(bg="blue")

        if self.plateau_ordinateur.tous_navires_coules():  # Si tous les navires ennemis sont coulés
            self._fin_de_partie("Victoire", "Vous avez gagné !")
        else:
            self.tour_joueur = False
            self._tour_ordinateur()

    # Tour de l'ordinateur (tirs automatiques)
    def _tour_ordinateur(self):
        x, y = random.randint(0, 9), random.randint(0, 9)
        while not self.plateau_joueur.tirer((x, y)):  # Réessaye jusqu'à trouver une case valide
            x, y = random.randint(0, 9), random.randint(0, 9)

        if self.plateau_joueur.tous_navires_coules():  # Si tous les navires du joueur sont coulés
            self._fin_de_partie("Défaite", "L'ordinateur a gagné !")
        else:
            self.tour_joueur = True

    # Fin de la partie et affichage d'un message
    def _fin_de_partie(self, titre, message):
        messagebox.showinfo(titre, message)
        self.nouvelle_partie()  # Relance une nouvelle partie

    # Réinitialisation complète pour une nouvelle partie
    def nouvelle_partie(self):
        self.__init__(self.root)


# Classe représentant le plateau de jeu
class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [["." for _ in range(taille)] for _ in range(taille)]  # Initialisation avec des cases vides
        self.navires = []

    def placer_navire(self, navire, position, orientation):
        x, y = position
        dx, dy = (1, 0) if orientation == "vertical" else (0, 1)
        cases = [(x + i * dx, y + i * dy) for i in range(navire.taille)]

        if all(0 <= cx < self.taille and 0 <= cy < self.taille for cx, cy in cases) and \
                all(self.grille[cx][cy] == "." for cx, cy in cases):  # Vérifie les cases disponibles
            for cx, cy in cases:
                self.grille[cx][cy] = "O"
            navire.positions = cases
            self.navires.append(navire)
            return True
        return False

    def tirer(self, position):
        x, y = position
        if self.grille[x][y] == "O":  # Touche un navire
            self.grille[x][y] = "X"
            return True
        elif self.grille[x][y] == ".":  # Case vide
            self.grille[x][y] = "-"
        return False

    def tous_navires_coules(self):
        return all(all(self.grille[x][y] == "X" for x, y in navire.positions) for navire in self.navires)


# Classe représentant un navire
class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []


# Classe représentant un joueur
class Joueur:
    def __init__(self, nom, plateau):
        self.nom = nom
        self.plateau = plateau


# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavaleApp(root)
    root.mainloop()
