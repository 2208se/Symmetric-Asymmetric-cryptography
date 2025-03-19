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
def permutep10(state):
    return [state[2], state[4], state[1], state[6], state[3], state[9], state[0], state[8], state[7], state[5]]

def permutep8(state):
    return [state[5], state[2], state[6], state[3], state[7], state[4], state[9], state[8]]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_keys(key):
    permuted_key = permutep10(key)

    left_half, right_half = permuted_key[:5], permuted_key[5:]

    left_half = left_shift(left_half, 1)
    right_half = left_shift(right_half, 1)

    k1 = permutep8(left_half + right_half)

    left_half = left_shift(left_half, 2)
    right_half = left_shift(right_half, 2)

    k2 = permutep8(left_half + right_half)

    return k1, k2  

key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]  
k1, k2 = generate_keys(key)

print("K1:", k1)
print("K2:", k2)


def permute_ip(bits):
    ip_table = [1, 5, 2, 0, 3, 7, 4, 6]  
    return [bits[i] for i in ip_table]


def expand_permute(bits):
    ep_table = [3, 0, 1, 2, 1, 2, 3, 0]
    return [bits[i] for i in ep_table]


def permute_p4(bits):
    p4_table = [1, 3, 2, 0]  
    return [bits[i] for i in p4_table]


def permute_ip_inverse(bits):
    ip_inv_table = [3, 0, 2, 4, 6, 1, 7, 5]  
    return [bits[i] for i in ip_inv_table]


def xor(bits, key):
    return [b ^ k for b, k in zip(bits, key)]


S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

def sbox_lookup(sbox, bits):
    row = int(f"{bits[0]}{bits[3]}", 2)
    col = int(f"{bits[1]}{bits[2]}", 2)
    return [int(b) for b in f"{sbox[row][col]:02b}"]

def substitute_sboxes(bits):
    left, right = bits[:4], bits[4:]  
    left_result = sbox_lookup(S0, left)
    right_result = sbox_lookup(S1, right)  
    return left_result + right_result  



def fK(left_half, right_half, key):
    ep_right = expand_permute(right_half)
    xored = xor(ep_right, key)  
    sbox_output = substitute_sboxes(xored)  
    p4_result = permute_p4(sbox_output)  
    new_left = xor(left_half, p4_result)
    return new_left, right_half  


def swap(left, right):
    return right, left  

def mini_des_encrypt(plaintext, k1, k2):
   
    permuted = permute_ip(plaintext)
    left, right = permuted[:4], permuted[4:]  

    left, right = fK(left, right, k1)

    left, right = swap(left, right)

    left, right = fK(left, right, k2)

    left, right = swap(left, right)
   
    ciphertext = permute_ip_inverse(left + right)
   
    return ciphertext




def mini_des_decrypt(ciphertext, k1, k2):
   
    permuted = permute_ip(ciphertext)
    left, right = permuted[:4], permuted[4:]  

    left, right = swap(left, right)

    left, right = fK(left, right, k2)

    left, right = swap(left, right)

    left, right = fK(left, right, k1)

    left, right = swap(left, right)
   
    ciphertext = permute_ip_inverse(left + right)
   
    return plaintext

plaintext = [0, 1, 1, 1, 0, 0, 1, 0]  

ciphertext = mini_des_encrypt(plaintext, k1, k2)
plaintext = mini_des_decrypt(ciphertext, k1, k2)
print("Ciphertext:", ''.join(map(str, ciphertext)))
print("Plain Text: ", ''.join(map(str, plaintext)))

