"""User management for the quiz application."""

__author__ = "caps_a"

import json
import os
from datetime import date

from utils import afficher_separateur, afficher_titre


class User:
    """Représente un utilisateur avec son nom et son historique de scores."""

    def __init__(self, nom: str):
        self._nom = nom
        self._scores = []  # liste de dict {"theme", "score", "date"}

    # --- Propriétés ---

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def scores(self) -> list:
        return self._scores

    # --- Méthodes ---

    def ajouter_score(
        self, theme: str, score: int, date_str: str = None
    ) -> None:
        """Ajoute un score à l'historique de l'utilisateur."""
        if date_str is None:
            date_str = date.today().isoformat()
        self._scores.append({"theme": theme, "score": score, "date": date_str})

    def afficher_historique(self) -> None:
        """Affiche l'historique des scores de l'utilisateur."""
        afficher_titre(f"Historique de {self._nom}")

        if not self._scores:
            print("\n  Aucune partie jouee pour le moment.\n")
            return

        print(f"\n  {'Theme':<20} {'Score':>8}   {'Date'}")
        afficher_separateur()
        for entree in self._scores:
            t = entree['theme']
            s = entree['score']
            d = entree['date']
            print(f"  {t:<20} {s:>7}%   {d}")
        afficher_separateur()

        # Statistiques par thème
        themes = set(e["theme"] for e in self._scores)
        print("\n  Moyennes par theme :")
        for theme in sorted(themes):
            scores_theme = [
                e["score"] for e in self._scores
                if e["theme"] == theme
            ]
            moyenne = round(sum(scores_theme) / len(scores_theme))
            nb = len(scores_theme)
            print(
                f"    - {theme:<18} : {moyenne}%"
                f" (sur {nb} partie(s))"
            )
        print()

    def to_dict(self) -> dict:
        """Sérialise l'utilisateur au format attendu par utilisateurs.json."""
        return {"scores": self._scores}

    @classmethod
    def from_dict(cls, nom: str, data: dict) -> "User":
        """Crée un User à partir d'un dict issu de utilisateurs.json."""
        utilisateur = cls(nom)
        utilisateur._scores = data.get("scores", [])
        return utilisateur


class UserManager:
    """Gère la persistance de tous les utilisateurs via un fichier JSON."""

    def __init__(self, fichier: str):
        self._fichier = fichier
        self._users: dict[str, User] = {}

    # --- Persistance ---

    def charger(self) -> None:
        """
        Charge les utilisateurs depuis le fichier JSON.
        Si le fichier est absent, démarre avec un dictionnaire vide.
        Lève ValueError si le JSON est corrompu.
        """
        if not os.path.exists(self._fichier):
            self._users = {}
            return

        with open(self._fichier, "r", encoding="utf-8") as f:
            try:
                donnees = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Fichier utilisateurs.json corrompu : {e}")

        if not isinstance(donnees, dict):
            raise ValueError(
                "Le fichier utilisateurs.json doit contenir un objet JSON."
            )

        self._users = {
            nom: User.from_dict(nom, data)
            for nom, data in donnees.items()
        }

    def sauvegarder(self) -> None:
        """Sauvegarde tous les utilisateurs dans le fichier JSON."""
        # Crée le dossier parent si nécessaire
        dossier = os.path.dirname(self._fichier)
        if dossier and not os.path.exists(dossier):
            os.makedirs(dossier)

        donnees = {nom: user.to_dict() for nom, user in self._users.items()}

        with open(self._fichier, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)

    # --- Gestion des utilisateurs ---

    def get_user(self, nom: str) -> User:
        """Retourne l'utilisateur par nom, le cree s'il n'existe pas."""
        if nom not in self._users:
            self._users[nom] = User(nom)
        return self._users[nom]

    def enregistrer_score(self, nom: str, theme: str, score: int) -> None:
        """Ajoute un score pour l'utilisateur et sauvegarde immédiatement."""
        user = self.get_user(nom)
        user.ajouter_score(theme, score)
        self.sauvegarder()

    def afficher_resultats(self, nom: str) -> None:
        """Affiche l'historique de scores d'un utilisateur."""
        user = self.get_user(nom)
        user.afficher_historique()

    def liste_utilisateurs(self) -> list:
        """Retourne la liste des noms d'utilisateurs enregistrés."""
        return sorted(self._users.keys())
