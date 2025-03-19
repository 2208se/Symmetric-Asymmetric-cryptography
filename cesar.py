import string
import unicodedata


def remove_accents(text):
   
    text = text.replace("'", "")  # Remove apostrophes
    text = text.replace(" ", "")  # Remove spaces from text
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def position(x):
    alphabet = string.ascii_lowercase
    x = x.lower()
    return alphabet.index(x) if x in alphabet else -1
print(position('a'))
print(position('!'))



def decalage(x, n):
    alphabet = string.ascii_lowercase
    if x.lower() not in alphabet:
        return x  # Keep non-alphabetic characters unchanged
    maj = x.isupper()
    new_pos = (position(x) + n) % 26
    new_char = alphabet[new_pos]
    return new_char.upper() if maj else new_char
print(decalage('a',2))



def codage(n, texte):
    texte = remove_accents(texte)  # Remove accents before encoding
    return ''.join(decalage(c, n) for c in texte)

def decodage(n, texte):
    return ''.join(decalage(c, -n) for c in texte)

# Test cases
print(codage(2, "élève à l'école"))
print(decodage(2, codage(2, "élève à l'école")))

# Message to encrypt
message = """La sécurité est une fonction incontournable des réseaux de communication. 
Elle consiste à éviter que des curieux puissent lire ou modifier les messages destinés à d'autre, 
ou des individus qui essaient d'utiliser des services en ligne auxquels ils ne sont pas autorisés à accéder."""

# Encrypting with a shift of 3
message_chiffre = codage(3, message)
print("Message chiffré :\n", message_chiffre)

# Decrypting
message_dechiffre = decodage(3, message_chiffre)
print("\nMessage déchiffré :\n", message_dechiffre)
