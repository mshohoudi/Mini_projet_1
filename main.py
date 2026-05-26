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

def chiffrer(message: str, cle: int) -> str:
    message_propre = normaliser_message(message)
    resultat = ""
    for char in message_propre:
        if char in alphabet:
            position = alphabet.index(char)
            resultat += alphabet[(position + cle) % 26]
        else:
            resultat += char
    return resultat


def dechiffrer(message: str, cle: int) -> str:
    message_propre = normaliser_message(message)
    resultat = ""
    for char in message_propre:
        if char in alphabet:
            position = alphabet.index(char)
            resultat += alphabet[(position - cle) % 26]
        else:
            resultat += char
    return resultat


def enigma_chiffrer(message: str, cles: tuple) -> str:
    # CORRECTIF : validation de la longueur de la clé
    if len(cles) != 3:
        return "Erreur, la clé n'a pas 3 chiffres"

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
    # CORRECTIF : validation de la longueur de la clé
    if len(cles) != 3:
        return "Erreur, la clé n'a pas 3 chiffres"

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


# CORRECTIF : nouvelle fonction pour chiffrer un fichier avec Enigma
def chiffrer_fichier_enigma(chemin_fichier: str, cles: tuple) -> str:
    """Lit un fichier texte et le chiffre avec Enigma César."""
    if len(cles) != 3:
        return "Erreur, la clé n'a pas 3 chiffres"

    with open(chemin_fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Chiffrer ligne par ligne pour conserver les sauts de ligne
    lignes = contenu.split("\n")
    lignes_chiffrees = [enigma_chiffrer(ligne, cles) for ligne in lignes]
    return "\n".join(lignes_chiffrees)


# =====================================================================
# FONCTIONS BRUTE-FORCE
# =====================================================================

MOTS_COURANTS_FR = {
    "le", "la", "les", "et", "de", "du", "un", "une", "est", "que",
    "dans", "pour", "au", "des", "qui", "sur", "en", "il", "ils",
    "leur", "leurs", "par", "pas", "plus", "se", "ce", "sont",
    "nous", "vous", "on", "mais", "ou", "donc", "car", "ni", "or",
    "avant", "apres", "avec", "sans", "sous", "vers", "entre", "sa",
    "ses", "mon", "ma", "mes", "ton", "ta", "tes", "cette", "cet",
    "nord", "sud", "ville", "point", "passer", "sera", "nord"
}


def score_francais(texte: str) -> float:
    """Retourne le ratio de mots français courants (entre 0 et 1)."""
    mots = re.findall(r'\b[a-z]+\b', texte)
    if not mots:
        return 0.0
    hits = sum(1 for m in mots if m in MOTS_COURANTS_FR)
    return hits / len(mots)


def est_francais(texte_dechiffre: str) -> bool:
    mots_texte = re.findall(r'\b[a-z]+\b', texte_dechiffre)
    total_mots = len(mots_texte)
    if total_mots == 0:
        return False
    score = sum(1 for mot in mots_texte if mot in MOTS_COURANTS_FR)
    seuil = max(3, int(total_mots / 4.5))
    return score >= seuil


def brute_force_cesar(message_chiffre: str):
    for cle in range(26):
        texte_essai = dechiffrer(message_chiffre, cle)
        if est_francais(texte_essai):
            return cle, texte_essai
    return None, "Clé introuvable"

MOTS_COURANTS_FR = {
    "le", "la", "les", "et", "de", "du", "un", "une", "est", "que",
    "dans", "pour", "au", "des", "qui", "sur", "en", "il", "ils",
    "leur", "leurs", "par", "pas", "plus", "se", "ce", "sont",
    "nous", "vous", "on", "mais", "ou", "donc", "car", "avant",
    "avec", "sans", "vers", "sa", "ses", "mon", "ma", "cette",
    "nord", "sud", "ville", "point", "sera"
}

def score_francais(texte: str) -> float:
    mots = re.findall(r'\b[a-z]+\b', texte)
    if not mots:
        return 0.0
    hits = sum(1 for m in mots if m in MOTS_COURANTS_FR)
    return hits / len(mots)

def brute_force_enigma(message_chiffre: str):
    """Retourne la clé avec le meilleur score français (pas juste la première)."""
    toutes_les_cles = itertools.product(range(26), repeat=3)
    meilleur_score = 0.0
    meilleur_cles = None
    meilleur_texte = None

    for cles in toutes_les_cles:
        texte_essai = enigma_dechiffrer(message_chiffre, cles)
        s = score_francais(texte_essai)
        if s > meilleur_score:
            meilleur_score = s
            meilleur_cles = cles
            meilleur_texte = texte_essai

    if meilleur_score >= 0.20:
        return meilleur_cles, meilleur_texte
    return None, "Clé introuvable"


# =====================================================================
# ALIAS — compatibilité avec les noms utilisés dans les tests
# =====================================================================
chiffrer_string_caesar = chiffrer
chiffrer_string_enigma = enigma_chiffrer


# =====================================================================
# CLI (LIGNE DE COMMANDE)
# =====================================================================

def _parse_cle(texte: str):
    if texte is None:
        return None
    # Découper sur le tiret qui suit un chiffre (séparateur Enigma)
    parties = re.split(r'(?<=\d)-', texte)
    if len(parties) == 3:
        return tuple(int(x) for x in parties)
    if len(parties) == 1:
        return int(texte)
    # Si 2 parties → clé Enigma incomplète, on laisse passer pour que
    # enigma_chiffrer lève l'erreur "n'a pas 3 chiffres"
    return tuple(int(x) for x in parties)


def main(argv=None):
    """Point d'entrée principal du programme en ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Mini-Projet A : chiffrement de César / Enigma César.")

    parser.add_argument(
        "action",
        choices=["chiffrer", "dechiffrer", "enigma_chiffrer", "enigma_dechiffrer", "bruteforce"],
        help="Opération à effectuer.")

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

    elif args.action == "enigma_chiffrer":
        if cle is None:
            resultat = "Erreur : Clé manquante pour Enigma (chiffrement)."
        else:
            resultat = enigma_chiffrer(contenu_message, cle)

    elif args.action == "enigma_dechiffrer":
        if cle is None:
            resultat = "Erreur : Clé manquante pour Enigma (déchiffrement)."
        else:
            resultat = enigma_dechiffrer(contenu_message, cle)

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
