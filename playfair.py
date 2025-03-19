import string
import string
import unicodedata

def remove_accents(text):
    """Supprime les accents, apostrophes et espaces du texte."""
    text = text.replace("'", "").replace(" ", "")  # Supprime les apostrophes et espaces
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def prepare_text(text, lang="fr"):
    """Prépare le texte en insérant 'X' entre les lettres doublées et en supprimant les espaces et accents."""
    text = remove_accents(text).upper().replace("W", "V") if lang == "fr" else remove_accents(text).upper().replace("J", "I")
    text = "".join(filter(str.isalpha, text))  # Supprime les caractères non alphabétiques

    modified_text = ""
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text) and text[i] == text[i + 1]:  # Si deux lettres identiques se suivent
            modified_text += a + 'X'
            i += 1  # Ne pas sauter la deuxième lettre
        else:
            b = text[i+1] if i + 1 < len(text) else 'X'
            modified_text += a + b
            i += 2

    return modified_text

def create_playfair_square(keyword, lang="fr"):
    """Crée la matrice Playfair à partir du mot-clé."""
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" if lang == "en" else "ABCDEFGHIKLMNOPQRSTUVXYZ"
    keyword = remove_accents(keyword).upper().replace("W", "V") if lang == "fr" else remove_accents(keyword).upper().replace("J", "I")
    keyword = "".join(dict.fromkeys(keyword))  # Supprime les doublons en conservant l'ordre
    matrix = keyword + "".join([c for c in alphabet if c not in keyword])
    return [list(matrix[i:i+5]) for i in range(0, 25, 5)]

def find_position(matrix, letter):
    """Trouve la position d'une lettre dans la matrice Playfair."""
    for row in range(5):
        if letter in matrix[row]:
            return row, matrix[row].index(letter)
    return None

def playfair_cipher(text, key, mode="encrypt", lang="fr"):
    """Chiffre ou déchiffre un texte avec le chiffrement de Playfair."""
    matrix = create_playfair_square(key, lang)
    text_pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    result = ""
    print(matrix)

    for a, b in text_pairs:
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:  # Même ligne
            result += matrix[row_a][(col_a + (1 if mode == "encrypt" else -1)) % 5]
            result += matrix[row_b][(col_b + (1 if mode == "encrypt" else -1)) % 5]
        elif col_a == col_b:  # Même colonne
            result += matrix[(row_a + (1 if mode == "encrypt" else -1)) % 5][col_a]
            result += matrix[(row_b + (1 if mode == "encrypt" else -1)) % 5][col_b]
        else:  # Rectangle
            result += matrix[row_a][col_b]
            result += matrix[row_b][col_a]

    return result

# 🔹 Exemple d'utilisation :
keyword = "SECURITE"
message = "MESSAGé"  # Avec un 'S' doublé
langue = "fr"

# Modification du message avec insertion de 'X'
modified_message = prepare_text(message, langue)
print("🔹 Message modifié (pré-traité) :", modified_message)

# Chiffrement
chiffre = playfair_cipher(modified_message, keyword, mode="encrypt", lang=langue)
print("🔹 Message chiffré :", chiffre)

# Déchiffrement
dechiffre = playfair_cipher(chiffre, keyword, mode="decrypt", lang=langue)
print("🔹 Message déchiffré :", dechiffre)
