import string  # Import the alphabet
import unicodedata


def remove_accents(text):
   
    text = text.replace("'", "")  # Remove apostrophes
    text = text.replace(" ", "")  # Remove spaces from text
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')



def vigenere_encrypt(texte, cle):
    alphabet = string.ascii_lowercase  # Define the alphabet
    texte = texte.lower()  # Convert everything to lowercase
    texte = remove_accents(texte)  # Remove accents before encoding
    cle = cle.lower()  # Convert key to lowercase
    texte_chiffre = []  # Empty list to store encrypted letters
    
    for i, lettre in enumerate(texte):  # Loop through the message
        if lettre in alphabet:
            decalage = alphabet.index(cle[i % len(cle)])  # Get shift from key
            new_pos = (alphabet.index(lettre) + decalage) % 26  # Apply shift
            texte_chiffre.append(alphabet[new_pos])  # Store new letter
        else:
            texte_chiffre.append(lettre)  # Keep letters not in alphabets unchanged
    
    return ''.join(texte_chiffre)  # Convert list to string and return it

def vigenere_decrypt(texte_chiffre, cle):
    alphabet = string.ascii_lowercase  # Define the alphabet
    cle = cle.lower()  # Convert key to lowercase
    texte_dechiffre = []  # Empty list to store decrypted letters
    
    for i, lettre in enumerate(texte_chiffre):  # Loop through the encrypted text
        if lettre in alphabet:
            decalage = alphabet.index(cle[i % len(cle)])  # Get shift from key
            new_pos = (alphabet.index(lettre) - decalage) % 26  # Reverse shift
            texte_dechiffre.append(alphabet[new_pos])  # Store new letter
        else:
            texte_dechiffre.append(lettre)
    
    return ''.join(texte_dechiffre)  # Convert list to string and return it

# 🔹 Testing the functions
message = "école superieure d'informatique"
key = "abc"

message_chiffre = vigenere_encrypt(message, key)
print("🔒 Message chiffré :", message_chiffre)  # Output: hfnlp

message_dechiffre = vigenere_decrypt(message_chiffre, key)
print("🔓 Message déchiffré :", message_dechiffre)  # Output: hello

