import string
alphabet = string.ascii_lowercase
def dechiffrer(message: str, cle: int):
    message = message.lower()
    resultat = ""
    for character in message:
        if character in alphabet:
            index = alphabet.index(character)
            resultat += alphabet[(index - cle) % 26]
        else:
            resultat += character
    return resultat
#Test
print(dechiffrer("Veni, vidi, vici!", 42))
