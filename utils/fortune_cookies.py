import random

fortunes = [
    "A regulatory surprise is coming your way 🍪",
    "No new orders, but good news is on the horizon 🌤️",
    "You will discover a footnote that changes everything 📘",
    "A silent PDF holds great power. Read wisely 🧐",
    "A delay is not a denial. Stay tuned 📡",
    "Your inbox will bring fortune tomorrow 💌",
    "The case you seek is seeking you 🔍"
]

def get_fortune():
    return random.choice(fortunes)
