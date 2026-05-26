import string
import unicodedata

alphabet = string.ascii_lowercase


def normaliser_message(message: str):
    """
    Enlève les accents et met tout en minuscules (consigne du prof)
    """
    mot_normalise = unicodedata.normalize('NFKD', message)
    mot_normalise = ''.join([c for c in mot_normalise if not unicodedata.combining(c)])
    return mot_normalise.lower()


# ALGORITHMES DE CÉSAR (Clé = Entier)
def chiffrer(message: str, cle: int):
    message_propre = normaliser_message(message)
    resultat = ""

    for char in message_propre:
        if char in alphabet:
            index = alphabet.index(char)
            resultat += alphabet[(index + cle) % 26]
        else:
            resultat += char

    return resultat


def dechiffrer(message: str, cle: int):
    message_propre = normaliser_message(message)
    resultat = ""

    for char in message_propre:
        if char in alphabet:
            index = alphabet.index(char)
            resultat += alphabet[(index - cle) % 26]
        else:
            resultat += char

    return resultat

#ALGORITHMES ENIGMA (Clé = Tuple de 3 entiers)

def enigma_chiffrer(message: str, cle: tuple):
    message_propre = normaliser_message(message)
    resultat = ""
    index_cle = 0

    for char in message_propre:
        if char in alphabet:
            decalage = cle[index_cle % 3]
            position_actuelle = alphabet.index(char)
            nouvelle_position = (position_actuelle + decalage) % 26

            resultat += alphabet[nouvelle_position]
            index_cle += 1  # Incrémente seulement si c'est une lettre
        else:
            resultat += char

    return resultat


def enigma_dechiffrer(message: str, cle: tuple):
    message_propre = normaliser_message(message)
    resultat = ""
    index_cle = 0

    for char in message_propre:
        if char in alphabet:
            decalage = cle[index_cle % 3]
            position_actuelle = alphabet.index(char)
            nouvelle_position = (position_actuelle - decalage) % 26

            resultat += alphabet[nouvelle_position]
            index_cle += 1  # Incrémente seulement si c'est une lettre
        else:
            resultat += char

    return resultat


