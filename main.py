"""
MGA802 — Mini-Projet A : Chiffrement de César
Fichier principal contenant toutes les fonctions cryptographiques et le CLI.
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


# =====================================================================
# FONCTIONS DE CHIFFREMENT / DÉCHIFFREMENT
# =====================================================================

def chiffrer(message: str, cle: int):
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
    message_propre = normaliser_message(message)
    resultat = ""
    for char in message_propre:
        if char in alphabet:
            position = alphabet.index(char)
            resultat += alphabet[(position - cle) % 26]
        else:
            resultat += char
    return resultat


def enigma_chiffrer(message: str, cles: tuple):
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


# =====================================================================
# FONCTIONS BRUTE-FORCE
# =====================================================================

def est_francais(texte_dechiffre: str) -> bool:
    mots_texte = re.findall(r'\b[a-z]+\b', texte_dechiffre)
    total_mots = len(mots_texte)

    if total_mots == 0:
        return False

    mots_courants = {"le", "la", "les", "et", "de", "du", "un", "une", "est", "que", "dans", "pour", "au", "des", "qui",
                     "sur"}
    score = sum(1 for mot in mots_texte if mot in mots_courants)

    # Seuil dynamique : min 3 mots, ou ~22% pour les longs textes
    seuil = max(3, int(total_mots / 4.5))
    return score >= seuil


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


# =====================================================================
# CLI (LIGNE DE COMMANDE)
# =====================================================================

def _parse_cle(texte: str):
    """Convertit l'argument --cle en clé utilisable."""
    if texte is None:
        return None
    if "-" in texte.lstrip("-"):
        return tuple(int(x) for x in texte.split("-"))
    return int(texte)


def main(argv=None):
    """Point d'entrée principal du programme en ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Mini-Projet A : chiffrement de César / Enigma César.")

    parser.add_argument(
        "action",
        choices=["chiffrer", "dechiffrer", "enigma", "bruteforce"],
        help="Opération à effectuer (chiffrer, dechiffrer, enigma ou bruteforce).")

    parser.add_argument(
        "message",
        help="Texte à traiter OU chemin vers un fichier texte (.txt).")

    parser.add_argument(
        "-c", "--cle", required=False,
        help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")

    args = parser.parse_args(argv)

    # === LECTURE DE FICHIER ===
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

    print(resultat)


if __name__ == "__main__":
    main()