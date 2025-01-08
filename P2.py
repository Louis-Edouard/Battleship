import tkinter as tk
from tkinter import messagebox


class Interface:
    def __init__(self, root):
        """
        Initialise l'interface utilisateur avec deux grilles.
        :param root: Fenêtre principale Tkinter.
        """
        self.root = root
        self.root.title("Bataille Navale")

        self.grille_joueur = []
        self.grille_ordi = []

        self.creer_grilles()
        self.creer_controles()

    def creer_grilles(self):
        """
        Crée deux grilles 10x10 pour le joueur et l'ordinateur.
        """
        # Plateau du joueur
        tk.Label(self.root, text="Plateau Joueur").grid(row=0, column=0)
        frame_joueur = tk.Frame(self.root)
        frame_joueur.grid(row=1, column=0)

        for x in range(10):
            ligne = []
            for y in range(10):
                bouton = tk.Button(
                    frame_joueur,
                    width=2,
                    height=1,
                    bg="lightblue",
                    command=lambda x=x, y=y: self.cliquer_joueur(x, y)
                )
                bouton.grid(row=x, column=y)
                ligne.append(bouton)
            self.grille_joueur.append(ligne)

        # Plateau de l'ordinateur
        tk.Label(self.root, text="Plateau Ordinateur").grid(row=0, column=1)
        frame_ordi = tk.Frame(self.root)
        frame_ordi.grid(row=1, column=1)

        for x in range(10):
            ligne = []
            for y in range(10):
                bouton = tk.Button(
                    frame_ordi,
                    width=2,
                    height=1,
                    bg="lightgray",
                    command=lambda x=x, y=y: self.cliquer_ordi(x, y)
                )
                bouton.grid(row=x, column=y)
                ligne.append(bouton)
            self.grille_ordi.append(ligne)

    def creer_controles(self):
        """
        Crée un bouton pour réinitialiser la partie.
        """
        bouton_nouvelle_partie = tk.Button(self.root, text="Nouvelle Partie", command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=2, column=0, columnspan=2, pady=10)

    def cliquer_joueur(self, x, y):
        """
        Action lors d'un clic sur le plateau du joueur.
        """
        messagebox.showinfo("Joueur", f"Case Joueur ({x}, {y}) cliquée !")

    def cliquer_ordi(self, x, y):
        """
        Action lors d'un clic sur le plateau de l'ordinateur.
        """
        messagebox.showinfo("Ordinateur", f"Case Ordinateur ({x}, {y}) cliquée !")

    def nouvelle_partie(self):
        """
        Réinitialise les grilles.
        """
        for ligne in self.grille_joueur:
            for bouton in ligne:
                bouton.configure(bg="lightblue")

        for ligne in self.grille_ordi:
            for bouton in ligne:
                bouton.configure(bg="lightgray")

        messagebox.showinfo("Nouvelle Partie", "Les grilles ont été réinitialisées !")


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
