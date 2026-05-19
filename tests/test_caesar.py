"""Tests pour le Mini-Projet A.

Ce fichier contient les chaînes de test officielles + quelques cas
limites. Ajoutez vos propres tests au fur et à mesure.

Pour lancer les tests :
    pip install pytest
    pytest -v
"""
import sys
from pathlib import Path

# Permet d'importer main.py depuis le dossier parent
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import dechiffrer  # noqa: E402
from chiffrer import chiffrer_string_caesar, chiffrer_string_enigma, chiffrer_fichier_enigma

# ---------- Chaînes de test officielles — César (spec §7) ----------

def test_cesar_officiel_cle_42():
    assert chiffrer_string_caesar("Veni, vidi, vici!", 42) == "ludy, lyty, lysy!"


def test_cesar_officiel_cle_neg_42():
    assert chiffrer_string_caesar("Veni, vidi, vici!", -42) == "foxs, fsns, fsms!"


# ---------- Chaîne de test officielle — Enigma César (spec §2.6) ----------

def test_enigma_officiel_maison():
    assert chiffrer_string_enigma("MAISON", (7, 16, 9)) == "tqrzew"



# ---------- Cas standards (à compléter par votre équipe) ----------

def test_cesar_round_trip():
    """Chiffrer puis déchiffrer doit redonner le message original."""
    msg = "Bonjour le monde !"
    assert dechiffrer(chiffrer(msg, 7), 7) == msg

def test_enigma_fichier_txt():
    assert chiffrer_fichier_enigma("tests/test_enigma_fichier_txt", (7, 16, 9)) == "tqrzew\ntqrzew\ntqrzew!"



def test_cesar_cle_zero_identite():
    """Une clé de 0 ne doit rien changer."""
    assert chiffrer_string_caesar("Tout pareil.", 0) == "tout pareil."


# TODO : ajoutez vos propres tests ci-dessous
#  - test pour les majuscules
#  - test pour les caractères spéciaux (accents, ponctuation)
#  - test pour les très grandes clés (positives et négatives)
#  - test pour le brute-force (César ET Enigma César)
#  - test que enigma_chiffrer rejette une clé qui n'a pas 3 nombres
