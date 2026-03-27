"""Utils for the quiz application."""

__author__ = "caps_a"

import os


def effacer_ecran() -> None:
    """Efface le terminal (Windows et Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def afficher_titre(titre: str, sous_titre: str = None) -> None:
    """Affiche un titre encadré."""
    largeur = 50
    print("\n" + "=" * largeur)
    print(f"  {titre.upper()}")
    if sous_titre:
        print(f"  {sous_titre}")
    print("=" * largeur)


def afficher_separateur(char: str = "-", largeur: int = 50) -> None:
    """Affiche une ligne de séparation."""
    print(char * largeur)


def saisie_choix(
    prompt: str, choix_valides: list, message_erreur: str = None
) -> str:
    """
    Demande une saisie et valide qu'elle fait partie des choix acceptés.
    Boucle jusqu'à obtenir une réponse valide.
    """
    while True:
        try:
            reponse = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInterruption détectée. Au revoir !")
            raise SystemExit(0)

        if reponse in choix_valides:
            return reponse

        opts = ", ".join(choix_valides)
        erreur = (
            message_erreur
            or f"Choix invalide. Options possibles : {opts}"
        )
        print(f"  [!] {erreur}")


def saisie_texte(prompt: str, min_len: int = 1) -> str:
    """
    Demande une saisie textuelle non vide.
    Boucle jusqu'à obtenir une réponse d'au moins min_len caractères.
    """
    while True:
        try:
            reponse = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInterruption détectée. Au revoir !")
            raise SystemExit(0)

        if len(reponse) >= min_len:
            return reponse

        print(
            f"  [!] La saisie doit contenir au moins {min_len} caractere(s)."
        )
