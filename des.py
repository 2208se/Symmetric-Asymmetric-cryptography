# Permutation tables
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]

# S-boxes
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]
S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

# Helper functions
def permute(block, table):
    return [block[i - 1] for i in table]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

# Key generation
def key_generation(key):
    # Apply P10 permutation
    key_ = permute(key, P10)
    
    # Split into left and right halves
    left = key_[:5]
    right = key_[5:]
    
    # Left shift both halves by 1
    left = left_shift(left, 1)
    right = left_shift(right, 1)
    
    # Combine and apply P8 to get K1
    combined = left + right
    key1 = permute(combined, P8)
    
    # Left shift both halves by 2
    left = left_shift(left, 2)
    right = left_shift(right, 2)
    
    # Combine and apply P8 to get K2
    combined = left + right
    key2 = permute(combined, P8)
    
    return key1, key2

# Binary conversion for S-boxes
def binary_(val):
    if val == 0:
        return "00"
    elif val == 1:
        return "01"
    elif val == 2:
        return "10"
    else:
        return "11"

# Feistel function
def function_(ar, key_):
    l = ar[:4]
    r = ar[4:]
    
    # Expand and permute
    ep = permute(r, EP)
    
    # XOR with key
    ar = [key_[i] ^ ep[i] for i in range(8)]
    
    # Split into left and right
    l_1 = ar[:4]
    r_1 = ar[4:]
    
    # S-box substitution
    row = int(f"{l_1[0]}{l_1[3]}", 2)
    col = int(f"{l_1[1]}{l_1[2]}", 2)
    val = S0[row][col]
    str_l = binary_(val)
    
    row = int(f"{r_1[0]}{r_1[3]}", 2)
    col = int(f"{r_1[1]}{r_1[2]}", 2)
    val = S1[row][col]
    str_r = binary_(val)
    
    # Combine and permute with P4
    r_ = [int(str_l[i]) for i in range(2)] + [int(str_r[i]) for i in range(2)]
    r_p4 = permute(r_, P4)
    
    # XOR with left half
    l = [l[i] ^ r_p4[i] for i in range(4)]
    output = l + r
    return output

# Swap function
def swap(array, n):
    l = array[:n]
    r = array[n:]
    return r + l

# Encryption function
def encryption(plaintext, key1, key2):
    # Initial permutation
    arr = permute(plaintext, IP)
    
    # First round
    arr1 = function_(arr, key1)
    after_swap = swap(arr1, len(arr1) // 2)
    
    # Second round
    arr2 = function_(after_swap, key2)
    
    # Final permutation
    ciphertext = permute(arr2, IP_inv)
    return ciphertext

# Decryption function
def decryption(ciphertext, key1, key2):
    # Initial permutation
    arr = permute(ciphertext, IP)
    
    # First round with key2
    arr1 = function_(arr, key2)
    after_swap = swap(arr1, len(arr1) // 2)
    
    # Second round with key1
    arr2 = function_(after_swap, key1)
    
    # Final permutation
    decrypted = permute(arr2, IP_inv)
    return decrypted

# Example usage
key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
plaintext = [0, 1, 1, 1, 0, 0, 1, 0]

# Generate keys
key1, key2 = key_generation(key)
print("Key-1:", key1)
print("Key-2:", key2)

# Encrypt
ciphertext = encryption(plaintext, key1, key2)
print("Ciphertext:", ciphertext)

# Decrypt
decrypted = decryption(ciphertext, key1, key2)
print("Decrypted:", decrypted)