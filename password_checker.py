import tkinter as tk
from tkinter import ttk
import re
import math

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0d0d0f"
CARD      = "#16161a"
BORDER    = "#2a2a35"
TEXT      = "#e8e6f0"
MUTED     = "#6b6880"
ACCENT    = "#7c6af7"

C_WEAK    = "#ff4d6d"
C_FAIR    = "#ff9f1c"
C_GOOD    = "#06d6a0"
C_STRONG  = "#7c6af7"
C_GREAT   = "#00b4d8"

FONT_HEAD = ("Georgia", 22, "bold")
FONT_SUB  = ("Courier New", 10)
FONT_BODY = ("Segoe UI", 10)
FONT_SM   = ("Segoe UI", 9)
FONT_MED  = ("Segoe UI", 11)
FONT_LG   = ("Segoe UI", 13, "bold")


# ── Strength Engine ───────────────────────────────────────────────────────────
def assess_password(pw: str) -> dict:
    checks = {
        "length_8":   len(pw) >= 8,
        "length_12":  len(pw) >= 12,
        "length_16":  len(pw) >= 16,
        "uppercase":  bool(re.search(r"[A-Z]", pw)),
        "lowercase":  bool(re.search(r"[a-z]", pw)),
        "digits":     bool(re.search(r"\d", pw)),
        "special":    bool(re.search(r"[^A-Za-z0-9]", pw)),
        "no_repeat":  not bool(re.search(r"(.)\1{2,}", pw)),
        "no_seq":     not bool(re.search(
                          r"(012|123|234|345|456|567|678|789|890|"
                          r"abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|"
                          r"jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|"
                          r"stu|tuv|uvw|vwx|wxy|xyz)", pw.lower())),
    }

    score = 0
    if checks["length_8"]:  score += 1
    if checks["length_12"]: score += 1
    if checks["length_16"]: score += 1
    if checks["uppercase"]: score += 1
    if checks["lowercase"]: score += 1
    if checks["digits"]:    score += 1
    if checks["special"]:   score += 2
    if checks["no_repeat"]: score += 1
    if checks["no_seq"]:    score += 1

    max_score = 11
    pct = score / max_score

    # Entropy estimate
    charset = 0
    if checks["lowercase"]: charset += 26
    if checks["uppercase"]: charset += 26
    if checks["digits"]:    charset += 10
    if checks["special"]:   charset += 32
    entropy = len(pw) * math.log2(charset) if charset and pw else 0

    if pct < 0.25:
        label, color, emoji, tip = "Weak", C_WEAK, "🔴", \
            "This password is very easy to crack."
    elif pct < 0.5:
        label, color, emoji, tip = "Fair", C_FAIR, "🟠", \
            "Better, but still vulnerable to attacks."
    elif pct < 0.7:
        label, color, emoji, tip = "Good", C_GOOD, "🟢", \
            "Decent password. A few tweaks can make it great."
    elif pct < 0.9:
        label, color, emoji, tip = "Strong", C_STRONG, "🟣", \
            "Strong password. Almost there!"
    else:
        label, color, emoji, tip = "Excellent", C_GREAT, "🔵", \
            "Exceptional password. Keep it safe!"

    suggestions = []
    if not checks["length_8"]:   suggestions.append("Use at least 8 characters")
    if not checks["length_12"]:  suggestions.append("Aim for 12+ characters")
    if not checks["length_16"]:  suggestions.append("16+ chars for maximum safety")
    if not checks["uppercase"]:  suggestions.append("Add uppercase letters (A–Z)")
    if not checks["lowercase"]:  suggestions.append("Add lowercase letters (a–z)")
    if not checks["digits"]:     suggestions.append("Include numbers (0–9)")
    if not checks["special"]:    suggestions.append("Add symbols like !@#$%^&*")
    if not checks["no_repeat"]:  suggestions.append("Avoid repeating characters (aaa)")
    if not checks["no_seq"]:     suggestions.append("Avoid sequences like 'abc' or '123'")

    return dict(score=score, max_score=max_score, pct=pct,
                label=label, color=color, emoji=emoji, tip=tip,
                entropy=entropy, checks=checks, suggestions=suggestions,
                length=len(pw))


# ── GUI ───────────────────────────────────────────────────────────────────────
class PasswordChecker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PassGuard — Password Strength Checker")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._show_pw = False
        self._build_ui()
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    # ── layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = tk.Frame(self, bg=BG, padx=28, pady=24)
        outer.pack(fill="both", expand=True)

        # Header
        hdr = tk.Frame(outer, bg=BG)
        hdr.pack(fill="x", pady=(0, 20))
        tk.Label(hdr, text="PassGuard", font=FONT_HEAD,
                 fg=ACCENT, bg=BG).pack(anchor="w")
        tk.Label(hdr, text="Real-time password strength analysis",
                 font=FONT_SUB, fg=MUTED, bg=BG).pack(anchor="w")

        # Input card
        card = tk.Frame(outer, bg=CARD, bd=0, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(fill="x", pady=(0, 16))
        inner = tk.Frame(card, bg=CARD, padx=16, pady=14)
        inner.pack(fill="x")

        tk.Label(inner, text="Enter Password", font=FONT_SM,
                 fg=MUTED, bg=CARD).pack(anchor="w", pady=(0, 6))

        row = tk.Frame(inner, bg=CARD)
        row.pack(fill="x")

        self._pw_var = tk.StringVar()
        self._pw_var.trace_add("write", lambda *_: self._on_change())

        self._entry = tk.Entry(row, textvariable=self._pw_var, show="●",
                               font=("Courier New", 14),
                               bg="#1e1e26", fg=TEXT,
                               insertbackground=ACCENT,
                               relief="flat", bd=0,
                               highlightthickness=1,
                               highlightbackground=BORDER,
                               highlightcolor=ACCENT)
        self._entry.pack(side="left", fill="x", expand=True,
                         ipady=10, ipadx=10)

        self._eye_btn = tk.Button(row, text="👁", font=("Segoe UI", 13),
                                  bg="#1e1e26", fg=MUTED,
                                  activebackground="#1e1e26",
                                  activeforeground=TEXT,
                                  relief="flat", bd=0, cursor="hand2",
                                  command=self._toggle_pw)
        self._eye_btn.pack(side="left", padx=(4, 0))

        # Strength bar row
        bar_row = tk.Frame(outer, bg=BG)
        bar_row.pack(fill="x", pady=(0, 16))

        self._bar_canvas = tk.Canvas(bar_row, height=8, bg=BORDER,
                                     highlightthickness=0, bd=0)
        self._bar_canvas.pack(fill="x")

        # Status row
        status = tk.Frame(outer, bg=BG)
        status.pack(fill="x", pady=(0, 16))

        self._emoji_lbl = tk.Label(status, text="—", font=("Segoe UI", 20),
                                   bg=BG, fg=MUTED)
        self._emoji_lbl.pack(side="left")

        mid = tk.Frame(status, bg=BG)
        mid.pack(side="left", padx=12, fill="x", expand=True)
        self._strength_lbl = tk.Label(mid, text="Awaiting input",
                                      font=FONT_LG, fg=TEXT, bg=BG)
        self._strength_lbl.pack(anchor="w")
        self._tip_lbl = tk.Label(mid, text="Type a password to begin.",
                                 font=FONT_SM, fg=MUTED, bg=BG,
                                 wraplength=340, justify="left")
        self._tip_lbl.pack(anchor="w")

        self._score_lbl = tk.Label(status, text="", font=FONT_SM,
                                   fg=MUTED, bg=BG)
        self._score_lbl.pack(side="right")

        # Stats grid
        stats_card = tk.Frame(outer, bg=CARD, bd=0,
                              highlightthickness=1, highlightbackground=BORDER)
        stats_card.pack(fill="x", pady=(0, 16))
        stats_inner = tk.Frame(stats_card, bg=CARD, padx=16, pady=12)
        stats_inner.pack(fill="x")

        tk.Label(stats_inner, text="STATISTICS", font=("Courier New", 8),
                 fg=MUTED, bg=CARD).grid(row=0, column=0, columnspan=4,
                                         sticky="w", pady=(0, 8))

        self._stat_vars = {}
        stat_items = [
            ("length",  "Length"),
            ("entropy", "Entropy (bits)"),
        ]
        for c, (key, name) in enumerate(stat_items):
            tk.Label(stats_inner, text=name, font=FONT_SM,
                     fg=MUTED, bg=CARD).grid(row=1, column=c*2, sticky="w",
                                             padx=(0, 4))
            v = tk.StringVar(value="—")
            self._stat_vars[key] = v
            tk.Label(stats_inner, textvariable=v, font=("Courier New", 11, "bold"),
                     fg=TEXT, bg=CARD).grid(row=1, column=c*2+1, sticky="w",
                                            padx=(0, 24))

        # Checklist
        cl_card = tk.Frame(outer, bg=CARD, bd=0,
                           highlightthickness=1, highlightbackground=BORDER)
        cl_card.pack(fill="x", pady=(0, 16))
        cl_inner = tk.Frame(cl_card, bg=CARD, padx=16, pady=12)
        cl_inner.pack(fill="x")

        tk.Label(cl_inner, text="CRITERIA", font=("Courier New", 8),
                 fg=MUTED, bg=CARD).grid(row=0, column=0, columnspan=4,
                                         sticky="w", pady=(0, 8))

        self._check_labels = {}
        criteria = [
            ("length_8",  "8+ chars"),
            ("length_12", "12+ chars"),
            ("length_16", "16+ chars"),
            ("uppercase", "Uppercase"),
            ("lowercase", "Lowercase"),
            ("digits",    "Numbers"),
            ("special",   "Symbols"),
            ("no_repeat", "No repeats"),
            ("no_seq",    "No sequences"),
        ]
        cols = 3
        for i, (key, label) in enumerate(criteria):
            r, c = divmod(i, cols)
            frm = tk.Frame(cl_inner, bg=CARD)
            frm.grid(row=r+1, column=c, sticky="w", padx=(0, 20), pady=2)
            dot = tk.Label(frm, text="◆", font=("Segoe UI", 8),
                           fg=MUTED, bg=CARD)
            dot.pack(side="left", padx=(0, 5))
            lbl = tk.Label(frm, text=label, font=FONT_SM, fg=MUTED, bg=CARD)
            lbl.pack(side="left")
            self._check_labels[key] = (dot, lbl)

        # Suggestions
        sug_card = tk.Frame(outer, bg=CARD, bd=0,
                            highlightthickness=1, highlightbackground=BORDER)
        sug_card.pack(fill="x", pady=(0, 4))
        sug_inner = tk.Frame(sug_card, bg=CARD, padx=16, pady=12)
        sug_inner.pack(fill="x")

        tk.Label(sug_inner, text="SUGGESTIONS", font=("Courier New", 8),
                 fg=MUTED, bg=CARD).pack(anchor="w", pady=(0, 6))

        self._sug_lbl = tk.Label(sug_inner, text="—",
                                 font=FONT_SM, fg=MUTED, bg=CARD,
                                 justify="left", wraplength=420)
        self._sug_lbl.pack(anchor="w")

        # Footer
        tk.Label(outer, text="PassGuard v1.0  •  All analysis is local — nothing leaves your device",
                 font=("Courier New", 8), fg="#3a3a50", bg=BG).pack(pady=(12, 0))

        self._entry.focus()

    # ── interactions ─────────────────────────────────────────────────────────
    def _toggle_pw(self):
        self._show_pw = not self._show_pw
        self._entry.config(show="" if self._show_pw else "●")
        self._eye_btn.config(fg=ACCENT if self._show_pw else MUTED)

    def _on_change(self):
        pw = self._pw_var.get()
        if not pw:
            self._reset_ui()
            return
        r = assess_password(pw)
        self._update_bar(r)
        self._update_status(r)
        self._update_stats(r)
        self._update_checks(r)
        self._update_suggestions(r)

    # ── UI updaters ───────────────────────────────────────────────────────────
    def _reset_ui(self):
        self._bar_canvas.delete("all")
        self._emoji_lbl.config(text="—", fg=MUTED)
        self._strength_lbl.config(text="Awaiting input", fg=TEXT)
        self._tip_lbl.config(text="Type a password to begin.")
        self._score_lbl.config(text="")
        for k in self._stat_vars:
            self._stat_vars[k].set("—")
        for dot, lbl in self._check_labels.values():
            dot.config(fg=MUTED)
            lbl.config(fg=MUTED)
        self._sug_lbl.config(text="—")

    def _update_bar(self, r):
        c = self._bar_canvas
        c.delete("all")
        c.update_idletasks()
        W = c.winfo_width() or 440
        H = 8
        # background rounded pill
        c.create_rectangle(0, 0, W, H, fill=BORDER, outline="", tags="bg")
        # filled portion
        fill_w = max(4, int(W * r["pct"]))
        c.create_rectangle(0, 0, fill_w, H, fill=r["color"], outline="")

    def _update_status(self, r):
        self._emoji_lbl.config(text=r["emoji"], fg=r["color"])
        self._strength_lbl.config(text=r["label"], fg=r["color"])
        self._tip_lbl.config(text=r["tip"])
        self._score_lbl.config(
            text=f"Score  {r['score']} / {r['max_score']}", fg=MUTED)

    def _update_stats(self, r):
        self._stat_vars["length"].set(str(r["length"]))
        self._stat_vars["entropy"].set(f"{r['entropy']:.1f}")

    def _update_checks(self, r):
        for key, (dot, lbl) in self._check_labels.items():
            passed = r["checks"][key]
            color = C_GOOD if passed else MUTED
            dot.config(fg=color)
            lbl.config(fg=color)

    def _update_suggestions(self, r):
        if r["suggestions"]:
            text = "  •  ".join(r["suggestions"][:4])
        else:
            text = "✓  Your password meets all recommended criteria!"
        self._sug_lbl.config(
            text=text,
            fg=C_GOOD if not r["suggestions"] else C_FAIR)


if __name__ == "__main__":
    app = PasswordChecker()
    app.mainloop()
