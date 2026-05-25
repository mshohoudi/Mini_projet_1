"""
MGA802 — Mini-Projet A : Chiffrement de César
Squelette de départ pour votre équipe. (Intégré avec Brute-force)
"""
import argparse
import os
import string
import unicodedata
import re
import itertools
from time import perf_counter

# Alphabet global (minuscules uniquement)
alphabet = string.ascii_lowercase


def normaliser_message(message: str) -> str:
    """Enlève les accents et convertit le texte en minuscules."""
    mot_normalise = unicodedata.normalize('NFKD', message)
    mot_normalise = ''.join([c for c in mot_normalise if not unicodedata.combining(c)])
    return mot_normalise.lower()


def chiffrer(message: str, cle: int):
    # TODO: retourner la chaîne chiffrée (type str).
    # Exigences visibles dans tests/test_caesar.py :
    # - test_cesar_officiel_cle_42
    # - test_cesar_officiel_cle_neg_42
    # - test_cesar_cle_zero_identite
    # Exemples attendus par les tests :
    # - chiffrer("Veni, vidi, vici!", 42) -> "Ludy, lyty, lysy!"
    # - chiffrer("Veni, vidi, vici!", -42) -> "Foxs, fsns, fsms!"
    # - chiffrer("Tout pareil.", 0) -> "Tout pareil."

    message_propre = normaliser_message(message)
    resultat = ""
    for char in message_propre:
        if char in alphabet:
            position = alphabet.index(char)
            resultat += alphabet[(position + cle) % 26]
        else:
            resultat += char
    return resultat


def dechiffrer(message: str, cle: int):
    # TODO: retourner la chaîne déchiffrée (type str).
    # Exigence visible dans tests/test_caesar.py :
    # - test_cesar_round_trip
    # Le test vérifie que dechiffrer(chiffrer(msg, 7), 7) == msg.

    message_propre = normaliser_message(message)
    resultat = ""
    for char in message_propre:
        if char in alphabet:
            position = alphabet.index(char)
            resultat += alphabet[(position - cle) % 26]
        else:
            resultat += char
    return resultat


def enigma_chiffrer(message: str, cles):
    # TODO: retourner la chaîne chiffrée Enigma César (type str).
    # Exigence visible dans tests/test_caesar.py :
    # - test_enigma_officiel_maison
    # Exemple attendu par le test :
    # - enigma_chiffrer("MAISON", (7, 16, 9)) -> "TQRZEW"

    message_propre = normaliser_message(message)
    resultat = ""
    idx = 0
    for char in message_propre:
        if char in alphabet:
            position = alphabet.index(char)
            resultat += alphabet[(position + cles[idx]) % 26]
            idx = (idx + 1) % 3
        else:
            resultat += char
    return resultat


def enigma_dechiffrer(message: str, cles: tuple) -> str:
    """Fonction ajoutée pour les besoins du brute-force Enigma"""
    message_propre = normaliser_message(message)
    resultat = ""
    idx = 0
    for char in message_propre:
        if char in alphabet:
            position = alphabet.index(char)
            resultat += alphabet[(position - cles[idx]) % 26]
            idx = (idx + 1) % 3
        else:
            resultat += char
    return resultat


# === FONCTIONS BRUTE-FORCE AJOUTÉES ===

def est_francais(texte_dechiffre: str) -> bool:
    mots_texte = re.findall(r'\b[a-z]+\b', texte_dechiffre)
    mots_courants = {"le", "la", "les", "et", "de", "du", "un", "une", "est", "que", "dans", "pour"}
    score = sum(1 for mot in mots_texte if mot in mots_courants)
    return score >= 3


def brute_force_cesar(message_chiffre: str):
    for cle in range(26):
        texte_essai = dechiffrer(message_chiffre, cle)
        if est_francais(texte_essai):
            return cle, texte_essai
    return None, "Clé introuvable"


def brute_force_enigma(message_chiffre: str):
    toutes_les_cles = itertools.product(range(26), repeat=3)
    for cles in toutes_les_cles:
        texte_essai = enigma_dechiffrer(message_chiffre, cles)
        if est_francais(texte_essai):
            return cles, texte_essai
    return None, "Clé introuvable"


def _parse_cle(texte: str):
    """Convertit l'argument --cle en clé utilisable."""
    # S'il n'y a pas de clé (cas du bruteforce), on retourne None
    if texte is None:
        return None

    if "-" in texte.lstrip("-"):
        return tuple(int(x) for x in texte.split("-"))
    return int(texte)


def main(argv=None):
    """Point d'entrée principal du programme en ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Mini-Projet A : chiffrement de César / Enigma César.")

    # Ajout de 'bruteforce' aux choix possibles
    parser.add_argument(
        "action",
        choices=["chiffrer", "dechiffrer", "enigma", "bruteforce"],
        help="Opération à effectuer (chiffrer, dechiffrer, enigma ou bruteforce).")

    # Mise à jour de la description pour inclure la lecture de fichier
    parser.add_argument(
        "message",
        help="Texte à traiter OU chemin vers un fichier texte (.txt).")

    # required passé à False pour permettre au bruteforce de fonctionner sans clé
    parser.add_argument(
        "-c", "--cle", required=False,
        help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")

    args = parser.parse_args(argv)

    # === LECTURE DE FICHIER (TODO Complété) ===
    contenu_message = args.message
    if os.path.isfile(args.message):
        with open(args.message, "r", encoding="utf-8") as fio:
            contenu_message = fio.read()

    cle = _parse_cle(args.cle)

    if args.action == "chiffrer":
        if cle is None:
            resultat = "Erreur : Clé manquante pour le chiffrement."
        else:
            resultat = chiffrer(contenu_message, cle)

    elif args.action == "dechiffrer":
        if cle is None:
            resultat = "Erreur : Clé manquante pour le déchiffrement."
        else:
            resultat = dechiffrer(contenu_message, cle)

    elif args.action == "enigma":
        if cle is None:
            resultat = "Erreur : Clé manquante pour Enigma."
        else:
            resultat = enigma_chiffrer(contenu_message, cle)

    elif args.action == "bruteforce":
        # === MODE BRUTE-FORCE (TODO Complété) ===
        resultat = "🚀 Lancement du Brute-Force...\n"

        tic = perf_counter()
        cle_c, res_c = brute_force_cesar(contenu_message)
        toc = perf_counter()

        if cle_c is not None:
            resultat += f"✅ Succès (César) ! Clé: {cle_c} | Temps: {toc - tic:.4f}s\nTexte: {res_c}"
        else:
            resultat += "⚠️ Échec César. Essai Enigma...\n"
            tic_e = perf_counter()
            cle_e, res_e = brute_force_enigma(contenu_message)
            toc_e = perf_counter()

            if cle_e is not None:
                resultat += f"✅ Succès (Enigma) ! Clés: {cle_e} | Temps: {toc_e - tic_e:.4f}s\nTexte: {res_e}"
            else:
                resultat += "❌ Impossible de décrypter le message."

    # Afficher le résultat (conservé tel quel)
    print(resultat)


if __name__ == "__main__":
    main()