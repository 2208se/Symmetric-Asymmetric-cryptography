import numpy as np




def remove_accents(text):
   
    text = text.replace("'", "")  # Remove apostrophes
    text = text.replace(" ", "")  # Remove spaces from text
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')




def mod_inverse(a, m):
    """Retourne l'inverse modulaire de a modulo m, ou None si non existant."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def is_valid_key(matrix):
    """Vérifie si la matrice est inversible dans Z_26."""
    det = int(round(np.linalg.det(matrix))) % 26  # Déterminant modulo 26
    return np.gcd(det, 26) == 1  # Vérifier si det est premier avec 26

def text_to_numbers(text):
    """Convertit une chaîne en liste de nombres (A=0, B=1, ..., Z=25)."""
    return [ord(c) - ord('A') for c in text.upper() if 'A' <= c <= 'Z']

def numbers_to_text(numbers):
    """Convertit une liste de nombres en texte."""
    return ''.join(chr(n + ord('A')) for n in numbers)

def hill_encrypt(text, key_matrix):
    
    """Chiffre le texte avec la méthode de Hill."""
    if not is_valid_key(key_matrix):
        raise ValueError("La clé n'est pas valide : son déterminant doit être premier avec 26.")
 
    text_numbers = text_to_numbers(text)
    while len(text_numbers) % 2 != 0:  # S'assurer que la taille est paire
        text_numbers.append(23)  # Ajouter 'X' (23) comme remplissage

    text_matrix = np.array(text_numbers).reshape(-1, 2)
    encrypted_matrix = np.dot(text_matrix, key_matrix) % 26
    encrypted_text = numbers_to_text(encrypted_matrix.flatten())
    print(encrypted_matrix)
    print(key_matrix)

    return encrypted_text

def hill_decrypt(cipher_text, key_matrix):
    """Déchiffre un texte chiffré avec la méthode de Hill."""
    if not is_valid_key(key_matrix):
        raise ValueError("La clé n'est pas valide : son déterminant doit être premier avec 26.")

    det = int(round(np.linalg.det(key_matrix))) % 26
    det_inv = mod_inverse(det, 26)
    
    if det_inv is None:
        raise ValueError("La matrice de clé n'a pas d'inverse dans Z_26.")
    
    # Calcul de l'inverse modulaire de la matrice clé
    adjugate = np.array([[key_matrix[1, 1], -key_matrix[0, 1]],
                         [-key_matrix[1, 0], key_matrix[0, 0]]])
    
    key_inv = (det_inv * adjugate) % 26
    key_inv = np.round(key_inv).astype(int)  # Assurer des entiers

    cipher_numbers = text_to_numbers(cipher_text)
    cipher_matrix = np.array(cipher_numbers).reshape(-1, 2)
    
    decrypted_matrix = np.dot(cipher_matrix, key_inv) % 26
    decrypted_text = numbers_to_text(decrypted_matrix.flatten())

    return decrypted_text

# 🔹 Exemple d'utilisation :
key_matrix_valid = np.array([[3, 3], [2, 5]])  # Clé 2x2 valide
message = "HELP"

print("Message original :", message)
encrypted_message = hill_encrypt(message, key_matrix_valid)
print("Message chiffré :", encrypted_message)

decrypted_message = hill_decrypt(encrypted_message, key_matrix_valid)
print("Message déchiffré :", decrypted_message)

# 🔹 Exemple de matrice non inversible :
key_matrix_invalid = np.array([[2, 4], [3, 6]])  # Déterminant = 0 (non premier avec 26)
print("\nTest de clé invalide :")
print("Clé invalide ?", not is_valid_key(key_matrix_invalid))
