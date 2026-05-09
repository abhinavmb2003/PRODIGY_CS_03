# 🔐 PassGuard — Password Strength Checker

A sleek, real-time **Python desktop GUI** that analyses password strength across 9 security criteria and gives instant, actionable feedback — all locally, with zero external dependencies.

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)

---

## ✨ Features

- **Live analysis** — updates on every keystroke, no button press needed
- **Animated strength bar** — colour-coded fill that reacts instantly
- **5 strength levels** — Weak 🔴 → Fair 🟠 → Good 🟢 → Strong 🟣 → Excellent 🔵
- **9-point security checklist** — length tiers, character variety, pattern detection
- **Entropy estimate** — shows bits of entropy based on charset × length
- **Smart suggestions** — up to 4 specific tips to improve the password
- **Show / Hide toggle** — 👁 button to reveal or mask input
- **100 % local** — nothing is transmitted; all logic runs offline

---

## 📋 Requirements

| Requirement | Version |
|---|---|
| Python | 3.6 or higher |
| tkinter | Included in standard Python |

No `pip install` needed — only Python's built-in standard library is used (`tkinter`, `re`, `math`).

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/passguard.git
cd passguard
```

### 2. Run the app

```bash
python password_checker.py
```

> On some Linux distros tkinter may need to be installed separately:
> ```bash
> sudo apt install python3-tk   # Debian / Ubuntu
> sudo dnf install python3-tkinter  # Fedora
> ```

---

## 🏗️ Project Structure

```
passguard/
├── password_checker.py   # Main application (single file)
├── README.md             # This file
├── requirements.txt      # Dependency list (empty — no deps)
├── .gitignore            # Python / OS ignores
└── LICENSE               # MIT License
```

---

## 🔢 Scoring System

The password receives a score out of **11 points**:

| Criterion | Points |
|---|---|
| Length ≥ 8 characters | +1 |
| Length ≥ 12 characters | +1 |
| Length ≥ 16 characters | +1 |
| Contains uppercase letters (A–Z) | +1 |
| Contains lowercase letters (a–z) | +1 |
| Contains digits (0–9) | +1 |
| Contains special characters (!@#…) | +2 |
| No repeated characters (aaa) | +1 |
| No sequential patterns (abc, 123) | +1 |

### Strength Levels

| Score % | Label | Colour |
|---|---|---|
| < 25 % | Weak | 🔴 Red |
| 25 – 49 % | Fair | 🟠 Orange |
| 50 – 69 % | Good | 🟢 Green |
| 70 – 89 % | Strong | 🟣 Purple |
| ≥ 90 % | Excellent | 🔵 Cyan |

---

## 📸 Screenshot

> *Dark-themed GUI with real-time strength bar, criteria checklist, entropy stats, and improvement suggestions.*

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
