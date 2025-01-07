class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []  # Positions occupées par le navire.
        self.touchees = 0    # Nombre de parties touchées.

    def est_coule(self):
        return self.touchees == self.taille


class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [["." for _ in range(taille)] for _ in range(taille)]  # "." pour vide
        self.navires = []  # Liste des navires.

    def placer_navire(self, navire, x, y, orientation):
        dx, dy = (1, 0) if orientation == "vertical" else (0, 1)
        positions = [(x + i * dx, y + i * dy) for i in range(navire.taille)]

        # Vérification de validité
        if any(cx < 0 or cy < 0 or cx >= self.taille or cy >= self.taille or self.grille[cx][cy] != "." 
               for cx, cy in positions):
            return False

        # Placement du navire
        for cx, cy in positions:
            self.grille[cx][cy] = "O"  # "O" pour navire
        navire.positions = positions
        self.navires.append(navire)
        return True

    def tirer(self, x, y):
        if self.grille[x][y] == "O":  # Touche un navire
            self.grille[x][y] = "X"
            for navire in self.navires:
                if (x, y) in navire.positions:
                    navire.touchees += 1
            return True
        elif self.grille[x][y] == ".":  # Eau
            self.grille[x][y] = "-"
        return False

    def tous_navires_coules(self):
        return all(navire.est_coule() for navire in self.navires)


class Joueur:
    def __init__(self, nom, plateau):
        self.nom = nom
        self.plateau = plateau

    def tirer(self, x, y, plateau_adverse):
        return plateau_adverse.tirer(x, y)
