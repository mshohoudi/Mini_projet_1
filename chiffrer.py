
import string
import unicodedata
alphabet = string.ascii_lowercase

def normaliser_message(message: str):
    """
    Fonction qui permet de normaliser une string pour en retirer les majuscules et les accents
    """

    """Solution obtenue sur : https://www.geeksforgeeks.org/python/how-to-remove-string-accents-using-python-3/"""

    # Normalize the string
    mot_normalise = unicodedata.normalize('NFKD', message)
    mot_normalise=''.join([c for c in mot_normalise if not unicodedata.combining(c)])
    return mot_normalise.lower()

def chiffrer_string_caesar(message: str, cle: int):
    """
    Fonction qui permet de chiffrer une string en chiffrement de caesar à partir d'une clé à un chiffre
    """
    message = normaliser_message(message)
    mot_chiffre =""

    #Boucle qui parcours la string et qui chiffre chaque lettre en conservant la ponctuation
    for i in message:
        if i.isalpha():
            #Chiffrement des lettres
            position=alphabet.find(i)

            lettre_chiffre = alphabet[(position+cle)%26]
            mot_chiffre += lettre_chiffre
        else:
            #Ajoute les caractères qui ne sont pas des lettres sans les chiffrer
            mot_chiffre += i


    return mot_chiffre



def chiffrer_string_enigma(message: str, cle: int):
    """
    Fonction qui permet de chiffrer une string en chiffrement enigma à partir d'une clé à 3 chiffres
    """
    if len(cle) !=3:
        #Renvoyer une erreur si la clé n'a pas 3 chiffres
        print("Erreur, la clé n'a pas 3 chiffres")
        return "Erreur, la clé n'a pas 3 chiffres"

    #Normaliser la string
    message = normaliser_message(message)

    mot_chiffre = ""
    index_cle=0

    # Boucle qui parcours la string et qui chiffre chaque lettre en conservant la ponctuation
    for i in message:

        if i.isalpha():
            # Chiffrement des lettres
            position = alphabet.find(i)
            lettre_chiffre = alphabet[(position + cle[index_cle]) % 26]
            mot_chiffre += lettre_chiffre
            index_cle += 1
        else:
            # Ajoute les caractères qui ne sont pas des lettres sans les chiffrer
            mot_chiffre += i

        if index_cle == len(cle):
            #Boucle pour parcourir les 3 clés en boucle
            index_cle =0


    return mot_chiffre

def chiffrer_fichier_caesar(chemin: str, cle: int):
    """
    Fonction qui permet de chiffrer un fichier en chiffrement caesar à partir d'une clé à 1 chiffre
    """

    #Ouverture, lecture et fermeture du fichier
    with open("message.txt", "r", encoding="utf-8") as fio:
        contenu = fio.read()
        fichier_chiffre=chiffrer_string_caesar(contenu, cle)

    with open(r"tests\test_caesar_fichier_encrypte.txt", "w", encoding="utf-8") as fio:
        fio.write(fichier_chiffre)

    return fichier_chiffre


def chiffrer_fichier_enigma(chemin: str, cle: int):
    """
    Fonction qui permet de chiffrer un fichier en chiffrement enigma à partir d'une clé à 3 chiffres
    """

    # Ouverture, lecture et fermeture du fichier
    with open(chemin, "r", encoding="utf-8") as fio:
        contenu = fio.read()

        #Chiffrage du fichier
        fichier_chiffre=chiffrer_string_enigma(contenu, cle)

    # Ouverture, écriture et fermeture du fichier chiffré
    with open(r"tests\test_enigma_fichier_encrypte.txt", "w", encoding="utf-8") as fio:
        fio.write(fichier_chiffre)
    return fichier_chiffre


#chiffrer_string_caesar("Le point de ralliement sera au nord de la ville de Rome avant de passer à l'attaque!", 42)
#print (f"Voici lemot normalisé : {normaliser_message("Épai,s")}")
#print (f"Le chiffrement de maison devrait être égal à tqrzew : {chiffrer_string_enigma("MAISON", (7, 16, 9))}")
#chiffrer_fichier_caesar("message.txt",42)
#chiffrer_fichier_enigma("message.txt",(7, 16, 9))
chiffrer_string_enigma("le secret est dans la boite",(3,12,21))