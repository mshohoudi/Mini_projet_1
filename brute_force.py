import string
import unicodedata
import re
import itertools
from time import perf_counter

alphabet = string.ascii_lowercase


# =====================================================================
# 1. FONCTIONS DE NORMALISATION ET DÉCHIFFREMENT
# =====================================================================

def normaliser_message(message: str):
    """
    Supprime les accents et convertit en minuscules.
    """
    mot_normalise = unicodedata.normalize('NFKD', message)
    mot_normalise = ''.join([c for c in mot_normalise if not unicodedata.combining(c)])
    return mot_normalise.lower()


def dechiffrer_string_caesar(message: str, cle: int):
    """
    Déchiffre un message César en utilisant la logique de l'équipe.
    """
    message_propre = normaliser_message(message)
    mot_dechiffre = ""
    for i in message_propre:
        if i.isalpha() and i in alphabet:
            position = alphabet.find(i)
            lettre_dechiffre = alphabet[(position - cle) % 26]
            mot_dechiffre += lettre_dechiffre
        else:
            mot_dechiffre += i
    return mot_dechiffre


def dechiffrer_string_enigma(message: str, cles: tuple):
    """
    Déchiffre un message Enigma César en utilisant la logique de l'équipe.
    """
    message_propre = normaliser_message(message)
    mot_dechiffre = ""
    index_cle = 0
    for i in message_propre:
        if i.isalpha() and i in alphabet:
            position = alphabet.find(i)
            lettre_dechiffre = alphabet[(position - cles[index_cle]) % 26]
            mot_dechiffre += lettre_dechiffre

            # Gestion de l'index de la clé
            index_cle += 1
            if index_cle == len(cles):
                index_cle = 0
        else:
            mot_dechiffre += i
    return mot_dechiffre


# =====================================================================
# 2. LOGIQUE DU BRUTE-FORCE ET DÉTECTION DU FRANÇAIS
# =====================================================================

def est_francais(texte_dechiffre: str):
    """
    Vérifie si le texte déchiffré est un texte français valide.
    Recherche basée sur des mots courants en minuscules.
    """
    # Extraction des mots purs en minuscules (le texte entrant est déjà normalisé)
    mots_texte = re.findall(r'\b[a-z]+\b', texte_dechiffre)

    # Dictionnaire de mots courants (Recherche O(1))
    mots_courants = {"le", "la", "les", "des", "et", "de", "du", "un", "une", "est", "que", "dans", "pour"}

    # Calcul du score
    score = sum(1 for mot in mots_texte if mot in mots_courants)

    # Validation (2 mots trouvés suffisent généralement)
    if score >= max((len(mots_texte)//4.5), 3):
        return True
    return False


def brute_force_cesar(message_chiffre: str):
    """
    Applique la méthode brute-force pour casser le chiffrement de César.
    """
    print("Démarrage du brute-force (César)...")

    for cle in range(26):
        # Déchiffrement avec la clé actuelle
        texte_essai = dechiffrer_string_caesar(message_chiffre, cle)

        # Vérification linguistique
        if est_francais(texte_essai):
            return cle, texte_essai

    return None, "Clé introuvable"


def brute_force_enigma(message_chiffre: str):
    """
    Applique la méthode brute-force pour casser Enigma César (17 576 possibilités).
    """
    print("Démarrage du brute-force (Enigma)...")

    toutes_les_cles = itertools.product(range(26), repeat=3)

    for cles in toutes_les_cles:
        texte_essai = dechiffrer_string_enigma(message_chiffre, cles)

        if est_francais(texte_essai):
            return cles, texte_essai

    return None, "Clé introuvable"


# =====================================================================
# 3. SECTION DE TEST ET MESURE DE PERFORMANCE
# =====================================================================

if __name__ == "__main__":
    # Phrase cible : "le secret est dans la boite"

    # 1. TEST CÉSAR (Chiffré avec la clé 7)
    message_test_cesar = "sl zljyla lza khuz sh ivpal"

    tic_cesar = perf_counter()
    cle_cesar, resultat_cesar = brute_force_cesar(message_test_cesar)
    toc_cesar = perf_counter()

    if cle_cesar is not None:
        print(f"✅ Succès César ! Clé trouvée : {cle_cesar}")
        print(f"📜 Texte décrypté : {resultat_cesar}")
    print(f"⏱️ Temps d'exécution (César) : {toc_cesar - tic_cesar:.4f} secondes\n")
    print("-" * 50 + "\n")

    # 2. TEST ENIGMA (Chiffré avec les clés (3, 12, 21))
    message_test_enigma = "oq nhomhf zvf ydzn om wruoh"

    tic_enigma = perf_counter()
    cles_enigma, resultat_enigma = brute_force_enigma(message_test_enigma)
    toc_enigma = perf_counter()

    if cles_enigma is not None:
        print(f"✅ Succès Enigma ! Clés trouvées : {cles_enigma}")
        print(f"📜 Texte décrypté : {resultat_enigma}")
    print(f"⏱️ Temps d'exécution (Enigma) : {toc_enigma - tic_enigma:.4f} secondes\n")