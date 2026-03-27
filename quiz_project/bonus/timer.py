"""Timer for the quiz application."""

__author__ = "caps_a"

import threading
import time


class Timer:
    """Un timer pour limiter le temps de reponse a une question."""

    def __init__(self):
        self._start_time = None
        self._end_time = None

    def demarrer(self) -> None:
        """Demarre le timer."""
        self._start_time = time.time()
        self._end_time = None

    def arreter(self) -> None:
        """Arrete le timer."""
        if self._start_time is not None:
            self._end_time = time.time()

    @property
    def duree(self) -> float:
        """Retourne la duree ecoulee en secondes."""
        if self._start_time is None:
            return 0.0
        if self._end_time is None:
            return time.time() - self._start_time
        return self._end_time - self._start_time

    def attendre_reponse(
        self, prompt: str, duree_max: int = 30
    ) -> str | None:
        """
        Affiche un compte a rebours et attend la saisie utilisateur.
        Retourne la saisie ou None si le temps est ecoule.
        """
        self.demarrer()
        _resultat = [None]
        _repondu = threading.Event()

        print(f"  [Timer] Temps restant : {duree_max:2d}s")

        def _lire():
            """Thread : attend la saisie de l'utilisateur."""
            try:
                _resultat[0] = input(prompt)
            except (EOFError, OSError):
                pass
            finally:
                _repondu.set()

        def _compte_a_rebours():
            """Thread : met a jour la ligne de compte a rebours."""
            for restant in range(duree_max - 1, -1, -1):
                if _repondu.wait(timeout=1):
                    break
                print(
                    f"\033[1A\r"
                    f"  [Timer] Temps restant : {restant:2d}s  "
                    f"\033[1B\r",
                    end="",
                    flush=True,
                )

        t_saisie = threading.Thread(target=_lire, daemon=True)
        t_affichage = threading.Thread(
            target=_compte_a_rebours, daemon=True
        )

        t_affichage.start()
        t_saisie.start()

        repondu_a_temps = _repondu.wait(timeout=duree_max)
        self.arreter()
        _repondu.set()
        if not repondu_a_temps:
            print(
                f"\033[1A\r  [Temps ecoule !]                  \033[1B",
                flush=True,
            )
            return None

        return _resultat[0]
