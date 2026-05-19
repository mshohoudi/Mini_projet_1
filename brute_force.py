
import unicodedata
import re
import itertools
from time import perf_counter



def enlever_caracteres_speciaux(mot):
    """
    Supprime les accents et les caractères spéciaux d'une chaîne.
     """
    normalized_word = unicodedata.normalize('NFKD', mot)
    return ''.join([char for char in normalized_word if not unicodedata.combining(char)])


def est_francais(texte_dechiffre):
    """
    Vérifie si le texte déchiffré est un texte français valide de manière autonome.
    Utilise une approche basée sur la fréquence des mots courants.
    """
    texte_propre = enlever_caracteres_speciaux(texte_dechiffre.upper())

    # Extraction des mots purs (ignorer la ponctuation comme les virgules, points, etc.) à l'aide de Regex
    mots_texte = re.findall(r'\b[A-Z]+\b', texte_propre)

    # Utilisation d'un ensemble (Set) au lieu d'une liste (List) pour une complexité de recherche O(1)
    mots_courants = {"LE", "LA", "LES", "ET", "DE", "DU", "UN", "UNE", "EST", "QUE", "DANS", "POUR"}

    # Calcul du nombre d'occurrences des mots courants dans le texte testé
    score = sum(1 for mot in mots_texte if mot in mots_courants)

    # Si au moins 2 mots courants sont trouvés, on considère que le décryptage est réussi
    # (Ce seuil peut être ajusté en fonction de la longueur moyenne des messages)
    if score >= 2:
        return True
    return False
def brute_force_cesar(message_chiffre):
    """
    Applique la méthode brute-force pour casser le chiffrement de César.
    Teste les 26 clés possibles de 0 à 25.
    """
    print("Démarrage du brute-force (César)...")

    for cle in range(26):
        # 1. Tenter de déchiffrer avec la clé actuelle
        # texte_essai = dechiffrer(message_chiffre, cle)
        texte_essai = ""

        # 2. Vérifier si le résultat a du sens en français
        if est_francais(texte_essai):
            return cle, texte_essai

    return None, "Clé introuvable"

