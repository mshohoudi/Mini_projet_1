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
#from main import dechiffrer  # noqa: E402

from chiffrer import chiffrer_string_caesar, chiffrer_string_enigma, chiffrer_fichier_enigma
from brute_force import brute_force_enigma, brute_force_cesar

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
    assert dechiffrer(chiffrer_string_caesar(msg, 7), 7) == msg

def test_enigma_fichier_txt():
    assert chiffrer_fichier_enigma("tests/test_enigma_fichier_txt", (7, 16, 9)) == "tqrzew\ntqrzew\ntqrzew!"


def test_cesar_cle_zero_identite():
    """Une clé de 0 ne doit rien changer."""
    assert chiffrer_string_caesar("Tout pareil.", 0) == "tout pareil."

def test_enigma_grande_cle_positive_maison():
    """On ajoute un grand chiffre à la clé qui est un multiple de 26 pour garder la même réponse mais avec une très grande clé"""
    assert chiffrer_string_enigma("MAISON", (7+15050212547*26, 16+12354698741288*26, 9+9925619781786*26)) == "tqrzew"

def test_enigma_grande_cle_negative_maison():
    """On soustrait un grand chiffre à la clé qui est un multiple de 26 pour garder la même réponse mais avec une très grande clé négative"""
    assert chiffrer_string_enigma("MAISON", (7-15050212547*26, 16-12354698741288*26, 9-9925619781786*26)) == "tqrzew"

def test_cesar_ponctuation_cle_16():
    """On ajoute de la ponctuation. Le ponctuation devrait apparaitre aussi dans la sortie"""
    assert chiffrer_string_caesar("Veni?&, vidi!!, vici()*-!", 16) == "ludy?&, lyty!!, lysy()*-!"

def test_cesar_caracteres_speciaux_cle_16():
    """Si des caractères spéciaux sont dans le message, ils seront filtrées et remplacés par des caractères non-spéciaux"""
    assert chiffrer_string_caesar("Vénî, vïdì, viçi", 16) == "ludy, lyty, lysy"

def test_enigma_cle_2_chiffres():
    """Valider que une erreur est renvoyée si la clé n'a pas 3 chiffres"""
    assert chiffrer_string_enigma("MAISON", (7, 16)) == "Erreur, la clé n'a pas 3 chiffres"

def test_brute_force_cesar_cle_42():
    """Le module de brute force devrait retourner la bonne clé et le bon mot. On accpete que la clé retourné soir le modulo de 42, donc 16"""
    assert brute_force_cesar("bu feydj tu hqbbyucudj iuhq qk deht tu bq lybbu tu hecu qlqdj tu fqiiuh q b'qjjqgku!")==(42%26,"le point de ralliement sera au nord de la ville de rome avant de passer a l'attaque!")

def test_brute_force_enigma_cle_5_3_25():
    """Le module de brute force devrait retourner la bonne clé et le bon mot. On accpete que la clé retourné soir le modulo de 42, donc 16"""
    assert brute_force_enigma("qh otlmy gd wdkqldrhmy vdwd zz qnwg cj oz alkqh cj unrh zadmy gd udrxhq f o'zywzvxd!")==((5,3,25),"le point de ralliement sera au nord de la ville de rome avant de passer a l'attaque!")



