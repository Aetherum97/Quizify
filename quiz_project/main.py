"""The main entry point for the quiz application."""

__author__ = "caps_a"

import os
import sys

# Force l'encodage UTF-8 sur le terminal Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")

from quiz import Quiz
from user import UserManager
from utils import (
    afficher_separateur,
    afficher_titre,
    effacer_ecran,
    saisie_choix,
    saisie_texte,
)

# --- Chemins des fichiers de données ---
_BASE = os.path.dirname(__file__)
QUESTIONS_FILE = os.path.join(_BASE, "data", "questions.json")
UTILISATEURS_FILE = os.path.join(_BASE, "data", "utilisateurs.json")


def choisir_theme() -> str | None:
    """Affiche les thèmes disponibles et laisse l'utilisateur en choisir un."""
    try:
        themes = Quiz.get_themes(QUESTIONS_FILE)
    except FileNotFoundError as e:
        print(f"\n  [!] {e}")
        return None

    afficher_titre("Choisir un theme")
    print()
    for i, theme in enumerate(themes, 1):
        print(f"  {i}. {theme}")
    print(f"  {len(themes) + 1}. Tous les themes")
    print()

    choix_valides = [str(i) for i in range(1, len(themes) + 2)]
    choix = saisie_choix("Votre choix : ", choix_valides)
    index = int(choix) - 1

    if index < len(themes):
        return themes[index]
    return None  # "Tous les themes"


def jouer(user_manager: UserManager, nom_utilisateur: str) -> None:
    """Lance une partie de quiz pour l'utilisateur connecté."""
    effacer_ecran()
    theme = choisir_theme()
    if theme is None and not _questions_disponibles():
        return

    effacer_ecran()
    quiz = Quiz(theme=theme, melanger=True)

    try:
        quiz.charger_questions(QUESTIONS_FILE)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n  [!] Impossible de charger les questions : {e}\n")
        input("Appuyez sur Entree pour revenir au menu...")
        return

    label = theme if theme else "Tous les themes"
    nb_q = len(quiz.questions)
    afficher_titre(
        "C'est parti !",
        f"Theme : {label}  -  {nb_q} question(s)"
    )

    try:
        quiz.jouer()
    except KeyboardInterrupt:
        print("\n\n  Quiz interrompu.")

    effacer_ecran()
    quiz.afficher_resume()

    score = quiz.score_pourcentage
    user_manager.enregistrer_score(nom_utilisateur, label, score)
    print(f"  Score sauvegarde : {score}%\n")
    input("Appuyez sur Entree pour revenir au menu...")


def voir_resultats(user_manager: UserManager, nom_utilisateur: str) -> None:
    """Affiche l'historique de scores de l'utilisateur connecté."""
    effacer_ecran()
    user_manager.afficher_resultats(nom_utilisateur)
    input("Appuyez sur Entree pour revenir au menu...")


def _questions_disponibles() -> bool:
    """Vérifie silencieusement que le fichier de questions existe."""
    if not os.path.exists(QUESTIONS_FILE):
        print(f"\n  [!] Fichier de questions introuvable : {QUESTIONS_FILE}\n")
        input("Appuyez sur Entree pour revenir au menu...")
        return False
    return True


def menu_principal(user_manager: UserManager, nom_utilisateur: str) -> None:
    """Boucle du menu interactif principal."""
    while True:
        effacer_ecran()
        afficher_titre("Quizify", f"Connecte en tant que : {nom_utilisateur}")
        print()
        print("  1. Jouer")
        print("  2. Voir mes resultats")
        print("  3. Quitter")
        print()
        afficher_separateur()

        choix = saisie_choix("Votre choix : ", ["1", "2", "3"])

        if choix == "1":
            jouer(user_manager, nom_utilisateur)
        elif choix == "2":
            voir_resultats(user_manager, nom_utilisateur)
        else:
            effacer_ecran()
            print("\n  Au revoir !\n")
            sys.exit(0)


def main() -> None:
    """Initialise l'application et lance le menu principal."""
    effacer_ecran()
    afficher_titre("Quizify", "Application de quiz interactif")

    # Chargement des utilisateurs
    user_manager = UserManager(UTILISATEURS_FILE)
    try:
        user_manager.charger()
    except ValueError as e:
        print(f"\n  [!] Erreur lors du chargement des utilisateurs : {e}")
        print("  Le fichier utilisateurs.json sera reinitialise.\n")
        # On repart avec un UserManager vide
        user_manager = UserManager(UTILISATEURS_FILE)

    # Identification de l'utilisateur
    print()
    nom_utilisateur = saisie_texte("Entrez votre nom d'utilisateur : ")

    menu_principal(user_manager, nom_utilisateur)


if __name__ == "__main__":
    main()
