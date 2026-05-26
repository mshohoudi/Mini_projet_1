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

from main import (
    chiffrer, dechiffrer,
    enigma_chiffrer, enigma_dechiffrer,
    chiffrer_string_caesar, chiffrer_string_enigma, chiffrer_fichier_enigma,
    brute_force_cesar, brute_force_enigma
)
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
    assert dechiffrer(chiffrer_string_caesar(msg, 7), 7) == msg.lower()

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
    """Le module de brute force devrait retourner la bonne clé et le bon texte."""
    assert brute_force_enigma("qh otlmy gd wdkqldrhmy vdwd zz qnwg cj oz alkqh cj unrh zadmy gd udrxhq f o'zywzvxd!")==((5,3,25),"le point de ralliement sera au nord de la ville de rome avant de passer a l'attaque!")

def test_brute_force_enigma_texte_100_mots_cle_5_3_25():
    """Le module de brute force devrait retourner la bonne clé et le bon texte."""
    assert brute_force_enigma("qhr wrlflmx rmy fnsvswxhy o’ts gdx skzv fwdmiv drshwhr ih k’fqsnttnwd. qhtw fhalknvzylns d cjetyh cfqr qd unokj gd wrlj, vhyxdj hm nwzqld, uxhx v’dxw dyhmixd fxstxq ih kf pdw pdilsjuqfqdj. odx unrdhsv dydhjqs whbtqmzv otxq qhtwv qtxsjv, kjxqx dpzhczfr jw kjxqx ezylljqsx lluudxvhtqmfqsx fnrpd qh btohxhd. qhtw dqrhd ilrhloqlmjh kjxq f sdwphx gd hrmvxdwlq ih mtpawhtc wdwuhyrhwhr. nor tqs fxrxl cjydqrouh cjv ktlr, zqd fglnqhxwqfwhtq dkihhdbj hs zqd qdmlxd, qh kfwhs, ttn d hsikzhmhh oqxrnhtwv kfqfzhr rrcjumjv. kf ftqwtwh qtpznqd ffbtucfls zqd luzsgd npotusfqbj d kf snqlsnttj, dtc ghjxw jw zza ruhbydbqhr uxaqlbx. o’drshwh qtpznq z rdqvxd ixqfekjpdsw k’mlryrhwh nhfhihmydkj.")==((5,3,25),"les romains ont construit l’un des plus grands empires de l’antiquite. leur civilisation a debute dans la ville de rome, situee en italie, puis s’est etendue autour de la mer mediterranee. les romains etaient reconnus pour leurs routes, leurs aqueducs et leurs batiments impressionnants comme le colisee. leur armee disciplinee leur a permis de conquerir de nombreux territoires. ils ont aussi developpe des lois, une administration efficace et une langue, le latin, qui a influence plusieurs langues modernes. la culture romaine accordait une grande importance a la politique, aux dieux et aux spectacles publics. l’empire romain a marque durablement l’histoire occidentale.")

def test_brute_force_enigma_texte_50_mots_cle_5_3_25():
    """Le module de brute force devrait retourner la bonne clé et le bon texte."""
    assert brute_force_enigma("qhr wrlflmx rmy gdahktsoj xm npljqrj hlulqj dtyrtw gd qd lju ljghyhqwdmjh. kjxqx vnqgzyv dydhjqs ilrhloqlmjv dy odzur nqfjqhjxqx fnsvswxhxdhjqs ihr wrtyhr, ihr urmyv dy gdx dpzhczfr. qd unokj gd wrlj hsfls qh bjqswh otohylpzh dy phqlsflqj gd hhs jponud uxhxvzsw. oqxrnhtwv kfqfzhr rrcjumjv owrunhmshmy hmhrqj dtortwg gzl cz ozylm udqqh zzwqjinnv ofu kjv qtpznqr.")==((5,3,25),"les romains ont developpe un immense empire autour de la mer mediterranee. leurs soldats etaient disciplines et leurs ingenieurs construisaient des routes, des ponts et des aqueducs. la ville de rome etait le centre politique et militaire de cet empire puissant. plusieurs langues modernes proviennent encore aujourd hui du latin parle autrefois par les romains.")

def test_brute_force_enigma_texte_25_mots_cle_5_3_25():
    """Le module de brute force devrait retourner la bonne clé et le bon texte."""
    assert brute_force_enigma("qhr wrlflmx fnsvswxhxdhjqs ihr wrtyhr xrkngdx hs ihr fttjgthv hrsqjvrnrmsdmyv. kjxq jponud irlnqznw oqxrnhtwv qjjhtqr jw kjxq hxkyxqj lmkotjqbf inwwdrhmy ognvstlqj htwrojhmsh ojqcfqs qrmlwdrsr.")==((5,3,25),"les romains construisaient des routes solides et des aqueducs impressionnants. leur empire dominait plusieurs regions et leur culture influenca fortement lhistoire europeenne pendant longtemps.")

