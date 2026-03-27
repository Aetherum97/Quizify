"""The quiz application."""

__author__ = "caps_a"

import json
import os
import random

from utils import afficher_separateur, afficher_titre, saisie_choix


class Question:
    """Représente une question du quiz avec ses options et sa bonne réponse."""

    def __init__(self, id: int, theme: str, question: str, options: list, reponse: str):
        self._id = id
        self._theme = theme
        self._question = question
        self._options = options
        self._reponse = reponse

    # --- Propriétés ---

    @property
    def id(self) -> int:
        return self._id

    @property
    def theme(self) -> str:
        return self._theme

    @property
    def question(self) -> str:
        return self._question

    @property
    def options(self) -> list:
        return self._options

    @property
    def reponse(self) -> str:
        return self._reponse

    # --- Méthode principale ---

    def verifier_reponse(self, reponse_utilisateur: str) -> bool:
        """Retourne True si la réponse de l'utilisateur est correcte."""
        return reponse_utilisateur.strip() == self._reponse.strip()

    def __str__(self) -> str:
        return f"Question {self._id} [{self._theme}] : {self._question}"


class Quiz:
    """Gère le déroulement d'un quiz : chargement, jeu et résumé des résultats."""

    def __init__(self, theme: str = None, melanger: bool = True):
        self._theme = theme
        self._melanger = melanger
        self._questions = []
        # Chaque élément : (Question, reponse_choisie: str, correct: bool)
        self._resultats = []

    # --- Propriétés ---

    @property
    def theme(self) -> str:
        return self._theme

    @property
    def questions(self) -> list:
        return self._questions

    @property
    def score(self) -> int:
        """Nombre de bonnes réponses."""
        return sum(1 for _, _, correct in self._resultats if correct)

    @property
    def score_pourcentage(self) -> int:
        """Score en pourcentage (0-100)."""
        if not self._questions:
            return 0
        return round(self.score / len(self._questions) * 100)

    # --- Chargement ---

    def charger_questions(self, fichier: str) -> None:
        """
        Charge les questions depuis un fichier JSON.
        Filtre par thème si self._theme est défini.
        Lève FileNotFoundError si le fichier est absent,
        ValueError si le JSON est invalide ou si aucune question n'est trouvée.
        """
        if not os.path.exists(fichier):
            raise FileNotFoundError(f"Fichier de questions introuvable : {fichier}")

        with open(fichier, "r", encoding="utf-8") as f:
            try:
                donnees = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Fichier JSON invalide : {e}")

        if not isinstance(donnees, list):
            raise ValueError("Le fichier JSON doit contenir une liste de questions.")

        questions = [
            Question(
                id=q["id"],
                theme=q["theme"],
                question=q["question"],
                options=q["options"],
                reponse=q["reponse"],
            )
            for q in donnees
        ]

        if self._theme:
            questions = [q for q in questions if q.theme.lower() == self._theme.lower()]

        if not questions:
            indication = f' pour le thème "{self._theme}"' if self._theme else ""
            raise ValueError(f"Aucune question trouvée{indication}.")

        if self._melanger:
            random.shuffle(questions)

        self._questions = questions

    @staticmethod
    def get_themes(fichier: str) -> list:
        """Retourne la liste triée des thèmes disponibles dans le fichier JSON."""
        if not os.path.exists(fichier):
            raise FileNotFoundError(f"Fichier de questions introuvable : {fichier}")

        with open(fichier, "r", encoding="utf-8") as f:
            donnees = json.load(f)

        return sorted(set(q["theme"] for q in donnees))

    # --- Jeu ---

    def _poser_question(self, question: Question, numero: int, total: int) -> bool:
        """Affiche une question, attend la réponse et retourne True si correcte."""
        afficher_separateur()
        print(f"\nQuestion {numero}/{total}  —  Theme : {question.theme}")
        print(f"\n  {question.question}\n")

        for i, option in enumerate(question.options, 1):
            print(f"    {i}. {option}")

        choix_valides = [str(i) for i in range(1, len(question.options) + 1)]
        choix = saisie_choix("\nVotre reponse (numero) : ", choix_valides)

        reponse_choisie = question.options[int(choix) - 1]
        correct = question.verifier_reponse(reponse_choisie)

        if correct:
            print("\n  [OK] Bonne reponse !")
        else:
            print(f"\n  [X]  Mauvaise reponse.")
            print(f"       Bonne reponse : {question.reponse}")

        self._resultats.append((question, reponse_choisie, correct))
        return correct

    def jouer(self) -> int:
        """
        Lance le quiz question par question.
        Retourne le score final en pourcentage.
        Lève RuntimeError si aucune question n'a été chargée.
        """
        if not self._questions:
            raise RuntimeError("Aucune question chargée. Appelez charger_questions() d'abord.")

        self._resultats = []
        total = len(self._questions)

        for i, question in enumerate(self._questions, 1):
            self._poser_question(question, i, total)
            if i < total:
                input("\nAppuyez sur Entree pour continuer...")

        return self.score_pourcentage

    # --- Résumé ---

    def afficher_resume(self) -> None:
        """Affiche le récapitulatif détaillé du quiz."""
        titre = f"RESUME — {self._theme}" if self._theme else "RESUME DU QUIZ"
        afficher_titre(titre)

        print(f"\n  Score final : {self.score}/{len(self._questions)} ({self.score_pourcentage}%)\n")
        afficher_separateur()

        for i, (question, reponse, correct) in enumerate(self._resultats, 1):
            statut = "[OK]" if correct else "[X] "
            enonce = question.question
            if len(enonce) > 55:
                enonce = enonce[:52] + "..."
            print(f"  {statut} Q{i}: {enonce}")
            if not correct:
                print(f"         Votre reponse  : {reponse}")
                print(f"         Bonne reponse  : {question.reponse}")

        afficher_separateur()

        if self.score_pourcentage == 100:
            message = "Score parfait ! Felicitations !"
        elif self.score_pourcentage >= 80:
            message = "Excellent resultat !"
        elif self.score_pourcentage >= 60:
            message = "Bon resultat, continuez ainsi !"
        elif self.score_pourcentage >= 40:
            message = "Peut mieux faire..."
        else:
            message = "Il faudra retravailler ce theme !"

        print(f"\n  {message}\n")
