
import string
import unicodedata
alphabet = string.ascii_lowercase

def normaliser_message(message: str):
    #Solution obtenue sur : https://www.geeksforgeeks.org/python/how-to-remove-string-accents-using-python-3/
    # Normalize the string
    mot_normalise = unicodedata.normalize('NFKD', message)
    mot_normalise=''.join([c for c in mot_normalise if not unicodedata.combining(c)])
    return mot_normalise.lower()

    print(res)

def chiffrer(message: str, cle: int):
    message = normaliser_message(message)
    mot_chiffre =""
    for i in message:
        if i.isalpha():
            position=alphabet.find(i)
            print(f"position de la lettre {i} est de {position}")

            lettre_chiffre = alphabet[(position+cle)%26]
            mot_chiffre += lettre_chiffre
        else:
            mot_chiffre += i

    print(f"mot chiffre est de {mot_chiffre}")
    return mot_chiffre



def enigma_chiffrer(message: str, cle: int):
    message = normaliser_message(message)
    print(f"longeur de la liset de clé : {len(cle)}")
    print(f"clé : {cle[1]}")
    mot_chiffre = ""
    index_cle=0
    for i in message:

        if i.isalpha():
            position = alphabet.find(i)
            print(f"position de la lettre {i} est de {position}")

            lettre_chiffre = alphabet[(position + cle[index_cle]) % 26]
            mot_chiffre += lettre_chiffre
            index_cle += 1
        else:
            mot_chiffre += i

        if index_cle == len(cle):
            index_cle =0

    print(f"mot chiffre est de {mot_chiffre}")
    return mot_chiffre

    return "allo"

#chiffrer("Veni, vidi, vici!", 42)
#print (f"Voici lemot normalisé : {normaliser_message("Épai,s")}")
#print (f"Le chiffrement de maison devrait être égal à tqrzew : {enigma_chiffrer("MAISON", (7, 16, 9))}")