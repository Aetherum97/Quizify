"""Connection to the bonus API for the quiz application."""

__author__ = "caps_a"

import html
import json
import random
import urllib.request

from quiz import Question

API_BASE = (
    "https://opentdb.com/api.php"
    "?amount=10&difficulty=easy&type=multiple"
)

# Correspondance nom affiche -> id categorie Open Trivia DB
CATEGORIES = {
    "General Knowledge": 9,
    "Entertainment: Books": 10,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Musicals & Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Science: Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Entertainment: Comics": 29,
    "Science: Gadgets": 30,
    "Entertainment: Anime & Manga": 31,
    "Entertainment: Cartoon & Animations": 32,
}


class ApiQuiz:
    """Charge des questions depuis l'API Open Trivia Database."""

    def __init__(self, categorie_id: int):
        self._categorie_id = categorie_id

    def _construire_url(self) -> str:
        """Construit l'URL avec la categorie choisie."""
        return f"{API_BASE}&category={self._categorie_id}"

    def _convertir_questions(self, resultats: list) -> list:
        """Convertit les resultats API au format Question."""
        questions = []
        for id_q, r in enumerate(resultats, 1):
            texte = html.unescape(r["question"])
            correct = html.unescape(r["correct_answer"])
            incorrects = [
                html.unescape(a) for a in r["incorrect_answers"]
            ]
            options = incorrects + [correct]
            random.shuffle(options)
            questions.append(Question(
                id=id_q,
                theme=html.unescape(r["category"]),
                question=texte,
                options=options,
                reponse=correct,
            ))
        return questions

    def charger(self) -> list | None:
        """
        Telecharge les questions depuis l'API.
        Retourne None si response_code != 0 ou en cas d'erreur reseau.
        """
        url = self._construire_url()
        try:
            with urllib.request.urlopen(url, timeout=5) as rep:
                data = json.loads(rep.read().decode("utf-8"))
        except Exception:
            return None

        if data.get("response_code") != 0:
            return None

        return self._convertir_questions(data["results"])
