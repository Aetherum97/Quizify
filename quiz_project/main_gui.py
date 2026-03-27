"""Interface graphique principale pour Quizify."""

__author__ = "caps_a"

import tkinter as tk

# --- Palette ---
BG = "#1e1e2e"       # Fond principal
BG_CARD = "#2a2a3e"  # Fond des cartes
ACCENT = "#7c3aed"   # Violet principal
ACCENT_H = "#6d28d9"  # Violet au survol
TEXT = "#e2e8f0"     # Texte principal
MUTED = "#94a3b8"    # Texte secondaire
ENTRY_BG = "#363656"  # Fond des champs
BTN_ALT = "#363656"  # Boutons secondaires
BTN_ALT_H = "#44446e"  # Boutons secondaires au survol
DANGER = "#ef4444"   # Rouge (Quitter)
DANGER_H = "#dc2626"  # Rouge au survol


class MenuPrincipal(tk.Tk):
    """Fenetre principale de l'application Quizify."""

    def __init__(self):
        super().__init__()
        self.title("Quizify")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._centrer(480, 580)
        self.nom_utilisateur = tk.StringVar()
        self._construire()

    # --- Initialisation ---

    def _centrer(self, w: int, h: int) -> None:
        """Centre la fenetre sur l'ecran au demarrage."""
        self.update_idletasks()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _construire(self) -> None:
        """Construit l'ensemble des sections de l'interface."""
        self._section_header()
        self._section_utilisateur()
        self._section_boutons()
        self._section_footer()

    # --- Sections ---

    def _section_header(self) -> None:
        """Titre, sous-titre et separateur de l'application."""
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="x", pady=(48, 18))

        tk.Label(
            frame,
            text="QUIZIFY",
            font=("Helvetica", 46, "bold"),
            fg=ACCENT,
            bg=BG,
        ).pack()

        tk.Label(
            frame,
            text="Le quiz interactif",
            font=("Helvetica", 13),
            fg=MUTED,
            bg=BG,
        ).pack(pady=(4, 18))

        # Separateur accent centre
        tk.Frame(frame, height=2, bg=ACCENT).pack(
            fill="x", padx=120
        )

    def _section_utilisateur(self) -> None:
        """Carte avec champ de saisie du nom d'utilisateur."""
        card = tk.Frame(self, bg=BG_CARD, padx=36, pady=22)
        card.pack(fill="x", padx=50, pady=(0, 18))

        tk.Label(
            card,
            text="Nom d'utilisateur",
            font=("Helvetica", 10),
            fg=MUTED,
            bg=BG_CARD,
            anchor="w",
        ).pack(fill="x")

        self._entry_nom = tk.Entry(
            card,
            textvariable=self.nom_utilisateur,
            font=("Helvetica", 14),
            bg=ENTRY_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=0,
        )
        self._entry_nom.pack(fill="x", ipady=9, pady=(6, 4))
        self._entry_nom.focus_set()

        # Soulignement accent sous le champ
        tk.Frame(card, height=2, bg=ACCENT).pack(fill="x")

    def _section_boutons(self) -> None:
        """Groupe des quatre boutons de navigation."""
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="x", padx=50)

        specs = [
            ("Jouer", ACCENT, ACCENT_H, None),
            ("Mes resultats", BTN_ALT, BTN_ALT_H, None),
            ("Classement", BTN_ALT, BTN_ALT_H, None),
            ("Quitter", DANGER, DANGER_H, self.destroy),
        ]

        for texte, bg, hover, cmd in specs:
            self._bouton(frame, texte, bg, hover, cmd)

    def _section_footer(self) -> None:
        """Pied de page discret avec version et source."""
        tk.Label(
            self,
            text="v1.0  —  Open Trivia DB",
            font=("Helvetica", 9),
            fg=MUTED,
            bg=BG,
        ).pack(side="bottom", pady=14)

    # --- Helpers ---

    def _bouton(
        self,
        parent: tk.Frame,
        texte: str,
        bg: str,
        hover: str,
        commande,
    ) -> tk.Button:
        """Cree un bouton stylise avec effet de survol."""
        btn = tk.Button(
            parent,
            text=texte,
            command=commande if commande else lambda: None,
            font=("Helvetica", 13, "bold"),
            fg=TEXT,
            bg=bg,
            activeforeground=TEXT,
            activebackground=hover,
            relief="flat",
            bd=0,
            pady=13,
            cursor="hand2",
        )
        btn.pack(fill="x", pady=5)
        btn.bind(
            "<Enter>",
            lambda e, b=btn, h=hover: b.config(bg=h)
        )
        btn.bind(
            "<Leave>",
            lambda e, b=btn, c=bg: b.config(bg=c)
        )
        return btn


if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()
