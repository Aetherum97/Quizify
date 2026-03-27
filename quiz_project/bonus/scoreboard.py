"""Scoreboard global CSV pour le quiz application."""

__author__ = "caps_a"

import csv
import os
from datetime import date

from utils import afficher_separateur, afficher_titre

CHAMPS = ["Utilisateur", "Theme", "Score", "Date"]


class Scoreboard:
    """Gere le classement global des joueurs via un fichier CSV."""

    def __init__(self, fichier: str):
        self._fichier = fichier
        self._entrees = []

    def charger(self) -> None:
        """
        Charge les entrees depuis le fichier CSV.
        Si absent, demarre avec une liste vide.
        """
        if not os.path.exists(self._fichier):
            self._entrees = []
            return

        with open(
            self._fichier, "r", encoding="utf-8", newline=""
        ) as f:
            lecteur = csv.DictReader(f)
            entrees = []
            for ligne in lecteur:
                try:
                    entrees.append({
                        "Utilisateur": ligne["Utilisateur"],
                        "Theme": ligne["Theme"],
                        "Score": int(ligne["Score"]),
                        "Date": ligne["Date"],
                    })
                except (KeyError, ValueError):
                    pass
            self._entrees = entrees

    def sauvegarder(self) -> None:
        """Sauvegarde toutes les entrees dans le fichier CSV."""
        dossier = os.path.dirname(self._fichier)
        if dossier and not os.path.exists(dossier):
            os.makedirs(dossier)

        with open(
            self._fichier, "w", encoding="utf-8", newline=""
        ) as f:
            writer = csv.DictWriter(f, fieldnames=CHAMPS)
            writer.writeheader()
            writer.writerows(self._entrees)

    def ajouter(
        self, utilisateur: str, theme: str, score: int
    ) -> None:
        """Ajoute une entree et sauvegarde immediatement."""
        self._entrees.append({
            "Utilisateur": utilisateur,
            "Theme": theme,
            "Score": score,
            "Date": date.today().isoformat(),
        })
        self.sauvegarder()

    def _entrees_triees(self, theme: str = None) -> list:
        """Retourne les entrees triees par score decroissant."""
        entrees = self._entrees
        if theme:
            entrees = [
                e for e in entrees if e["Theme"] == theme
            ]
        return sorted(
            entrees, key=lambda e: e["Score"], reverse=True
        )

    def afficher_classement(
        self, theme: str = None, limite: int = 10
    ) -> None:
        """Affiche le classement, filtre par theme si fourni."""
        titre = (
            f"CLASSEMENT — {theme}" if theme else "CLASSEMENT GENERAL"
        )
        afficher_titre(titre)

        entrees = self._entrees_triees(theme)[:limite]

        if not entrees:
            print("\n  Aucune entree dans le classement.\n")
            return

        print(
            f"\n  {'Rang':<6} {'Joueur':<18}"
            f" {'Theme':<16} {'Score':>6}   {'Date'}"
        )
        afficher_separateur()

        for rang, e in enumerate(entrees, 1):
            print(
                f"  {rang:<6} {e['Utilisateur']:<18}"
                f" {e['Theme']:<16} {e['Score']:>5}%"
                f"   {e['Date']}"
            )

        afficher_separateur()
        print()
