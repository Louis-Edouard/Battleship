import tkinter as tk
import random
from tkinter import messagebox


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")

        self.navires = [5, 4, 3, 3, 2, 2]  # Taille des navires
        self.orientation = "horizontal"

        self.grille_joueur = [[None for _ in range(10)] for _ in range(10)]
        self.grille_ordi = [[None for _ in range(10)] for _ in range(10)]
        self.navires_restants = list(self.navires)  # Copies des tailles à placer

        self.creer_grilles()
        self.placer_navires_ordi()

    def creer_grilles(self):
        """
        Crée deux grilles pour le joueur et l'ordinateur.
        """
        # Plateau du joueur
        frame_joueur = tk.Frame(self.root)
        frame_joueur.grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame_joueur, text="Joueur").pack()
        for x in range(10):
            for y in range(10):
                bouton = tk.Button(
                    frame_joueur,
                    width=2,
                    height=1,
                    bg="lightblue",
                    command=lambda x=x, y=y: self.placer_navire_joueur(x, y)
                )
                bouton.grid(row=x, column=y)
                self.grille_joueur[x][y] = bouton

        # Plateau de l'ordinateur (désactivé pour cette phase)
        frame_ordi = tk.Frame(self.root)
        frame_ordi.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(frame_ordi, text="Ordinateur").pack()
        for x in range(10):
            for y in range(10):
                bouton = tk.Button(frame_ordi, width=2, height=1, bg="lightgray", state=tk.DISABLED)
                bouton.grid(row=x, column=y)
                self.grille_ordi[x][y] = bouton

        # Bouton pour changer orientation
        tk.Button(self.root, text="Changer Orientation", command=self.changer_orientation).grid(row=1, column=0, pady=10)

    def placer_navire_joueur(self, x, y):
        """
        Permet au joueur de placer un navire sur son plateau.
        """
        if not self.navires_restants:
            messagebox.showinfo("Placement terminé", "Tous les navires sont placés !")
            return

        taille = self.navires_restants[0]

        if self.peut_placer(self.grille_joueur, x, y, taille, self.orientation):
            self.placer(self.grille_joueur, x, y, taille, self.orientation, "blue")
            self.navires_restants.pop(0)
            if not self.navires_restants:
                messagebox.showinfo("Placement terminé", "Placement terminé, à vous de jouer !")
        else:
            messagebox.showerror("Erreur", "Impossible de placer le navire ici.")

    def placer_navires_ordi(self):
        """
        Place les navires de l'ordinateur aléatoirement.
        """
        for taille in self.navires:
            place = False
            while not place:
                x, y = random.randint(0, 9), random.randint(0, 9)
                orientation = random.choice(["horizontal", "vertical"])
                if self.peut_placer(self.grille_ordi, x, y, taille, orientation):
                    self.placer(self.grille_ordi, x, y, taille, orientation, "gray")
                    place = True

    def peut_placer(self, grille, x, y, taille, orientation):
        """
        Vérifie si un navire peut être placé à l'emplacement donné.
        """
        if orientation == "horizontal":
            if y + taille > 10: return False
            return all(grille[x][y + i]["bg"] == "lightblue" for i in range(taille))
        else:
            if x + taille > 10: return False
            return all(grille[x + i][y]["bg"] == "lightblue" for i in range(taille))

    def placer(self, grille, x, y, taille, orientation, couleur):
        """
        Place un navire sur la grille.
        """
        if orientation == "horizontal":
            for i in range(taille):
                grille[x][y + i].configure(bg=couleur)
        else:
            for i in range(taille):
                grille[x + i][y].configure(bg=couleur)

    def changer_orientation(self):
        """
        Alterne entre horizontal et vertical pour le placement.
        """
        self.orientation = "vertical" if self.orientation == "horizontal" else "horizontal"
        messagebox.showinfo("Orientation", f"Orientation changée à {self.orientation}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
