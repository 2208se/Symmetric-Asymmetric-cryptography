# Mini-AES S-Box (Nibble Substitution Table)
S_BOX = {
    0b0000: 0b1110, 0b0001: 0b0100, 0b0010: 0b1101, 0b0011: 0b0001,
    0b0100: 0b0010, 0b0101: 0b1111, 0b0110: 0b1011, 0b0111: 0b1000,
    0b1000: 0b0011, 0b1001: 0b1010, 0b1010: 0b0110, 0b1011: 0b1100,
    0b1100: 0b0101, 0b1101: 0b1001, 0b1110: 0b0000, 0b1111: 0b0111
}

# Round Constants
RCON = [0b0001, 0b0010]  # rcon(1) = 0001, rcon(2) = 0010

def sub_nibble(nibble):
    """Apply Mini-AES S-Box to a 4-bit nibble."""
    return S_BOX[nibble]

def key_expansion(k0):
    """Generate K1 and K2 from K0 using Mini-AES key expansion with 4-bit nibbles."""
    # Step 1: Split K0 into four 4-bit words
    w = [(k0 >> (12 - 4 * i)) & 0xF for i in range(4)]

    # Step 2: Compute K1 Words
    w.append(w[0] ^ sub_nibble(w[3]) ^ RCON[0])  # w4
    w.append(w[1] ^ w[4])  # w5
    w.append(w[2] ^ w[5])  # w6
    w.append(w[3] ^ w[6])  # w7

    # Step 3: Compute K2 Words
    w.append(w[4] ^ sub_nibble(w[7]) ^ RCON[1])  # w8
    w.append(w[5] ^ w[8])  # w9
    w.append(w[6] ^ w[9])  # w10
    w.append(w[7] ^ w[10])  # w11

    # Convert words to full keys
    k1 = (w[4] << 12) | (w[5] << 8) | (w[6] << 4) | w[7]
    k2 = (w[8] << 12) | (w[9] << 8) | (w[10] << 4) | w[11]

    return k1, k2

# Given key
K0 = 0xC3F0  # 1100 0011 1111 0000

# Generate K1 and K2
K1, K2 = key_expansion(K0)

# Print results in binary and hex format
print(f"K1 = {K1:016b} ({K1:04X})")
print(f"K2 = {K2:016b} ({K2:04X})")






# Mini-AES S-Box (Nibble Substitution)
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

# Mini-AES Inverse S-Box (for decryption if needed)
INV_S_BOX = {v: k for k, v in S_BOX.items()}

# MixColumns matrix (GF(2⁴) operations)
MIX_COLUMNS_MATRIX = [[3, 2], [2, 3]]  # Defined in Mini-AES

def sub_nibbles(state):
    add_round_key(PLAINTEXT, K0)
    """Apply S-Box substitution to each nibble in the 16-bit state."""
    return (S_BOX[(state >> 12) & 0xF] << 12) | \
           (S_BOX[(state >> 8) & 0xF] << 8) | \
           (S_BOX[(state >> 4) & 0xF] << 4) | \
           (S_BOX[state & 0xF])



def sub_nibbles_inverse(state):
    add_round_key(PLAINTEXT, K0)
    """Apply S-Box substitution to each nibble in the 16-bit state."""
    return (INV_S_BOX[(state >> 12) & 0xF] << 12) | \
           (INV_S_BOX[(state >> 8) & 0xF] << 8) | \
           (INV_S_BOX[(state >> 4) & 0xF] << 4) | \
           (INV_S_BOX[state & 0xF])



def shift_row(state):
    """Swap the second nibble in the state."""
    return (state & 0xF000) | ((state & 0x00F0) << 4) | ((state & 0x0F00) >> 4) | (state & 0x000F)

def gf_mult(a, b):
    """Multiply two 4-bit numbers in GF(2⁴) using polynomial arithmetic and reduce modulo x⁴ + x + 1."""
    p = 0
    for i in range(4):
        if (b & 1):  # If the lowest bit of b is set
            p ^= a   # XOR with a (add in GF(2))
        carry = a & 0x8  # Check if x³ term is set
        a = (a << 1) & 0xF  # Shift left (mod 16 to keep 4-bit size)
        if carry:
            a ^= 0b0011  # Reduce by x⁴ + x + 1
        b >>= 1  # Shift right to process next bit
    return p

def mix_columns(state):
    """Perform the MixColumns transformation using GF(2⁴) multiplication."""
    # Extract nibbles
    s0, s1, s2, s3 = (state >> 12) & 0xF, (state >> 8) & 0xF, (state >> 4) & 0xF, state & 0xF
    
    # Matrix multiplication in GF(2⁴)
    s0_new = gf_mult(3, s0) ^ gf_mult(2, s2)
    s1_new = gf_mult(3, s1) ^ gf_mult(2, s3)
    s2_new = gf_mult(2, s0) ^ gf_mult(3, s2)
    s3_new = gf_mult(2, s1) ^ gf_mult(3, s3)

    return (s0_new << 12) | (s1_new << 8) | (s2_new << 4) | s3_new

def add_round_key(state, key):
    """XOR the state with the round key."""
    return state ^ key

def mini_aes_encrypt(plaintext, k0, k1, k2):
    """Encrypt a 16-bit plaintext using Mini-AES."""
    # Initial AddRoundKey
    state = add_round_key(plaintext, k0)

    # Round 1
    state = sub_nibbles(state)
    state = shift_row(state)
    state = mix_columns(state)
    state = add_round_key(state, k1)

    # Final Round (No MixColumns)
    state = sub_nibbles(state)
    state = shift_row(state)
    state = add_round_key(state, k2)

    return state

# Example Usage
K0 = 0xC3F0  # Example 16-bit key
K1, K2 = key_expansion(K0)

PLAINTEXT = 0xBEEF  # Example plaintext

CIPHERTEXT = mini_aes_encrypt(PLAINTEXT, K0, K1, K2)

# Print results
print(f"Plaintext:  {PLAINTEXT:016b} ({PLAINTEXT:04X})")
print(f"Ciphertext: {CIPHERTEXT:016b} ({CIPHERTEXT:04X})")









def print_matrix(label, value):
    """Print a 16-bit value as a 2×2 matrix in both hexadecimal and binary."""
    s0, s1, s2, s3 = (value >> 12) & 0xF, (value >> 8) & 0xF, (value >> 4) & 0xF, value & 0xF
    print(f"\n{label}:")
    print(f"Hex:   [ {s0:X}  {s1:X} ]      Binary: [ {s0:04b}  {s1:04b} ]")
    print(f"       [ {s2:X}  {s3:X} ]              [ {s2:04b}  {s3:04b} ]")



# Example usage in encryption
K0 = 0xC3F0  # Initial 16-bit key
PLAINTEXT = 0xBEEF  # Example 16-bit plaintext

# Key Expansion
K1, K2 = key_expansion(K0)

# Print Initial Matrices
print_matrix("Plaintext", PLAINTEXT)
print_matrix("Initial Key K0", K0)
print_matrix("Round Key K1", K1)
print_matrix("Round Key K2", K2)



state = add_round_key(PLAINTEXT, K0)
print_matrix("After AddRoundKey (K0)", state)

state = sub_nibbles(state)
print_matrix("After SubNibbles", state)

state = shift_row(state)
print_matrix("After ShiftRow", state)

state = mix_columns(state)
print_matrix("After MixColumns", state)

state = add_round_key(state, K1)
print_matrix("After AddRoundKey (K1)", state)

state = sub_nibbles(state)
print_matrix("After Final SubNibbles", state)

state = shift_row(state)
print_matrix("After Final ShiftRow", state)

state = add_round_key(state, K2)
print_matrix("Final Ciphertext", state)





def mini_aes_decrypt(plaintext, k0, k1, k2):
    """Encrypt a 16-bit plaintext using Mini-AES."""
    # Initial AddRoundKey
    state = add_round_key(ciphertext, k2)
    state = shift_row(state)
    state = sub_nibbles_inverse(state)
    state = add_round_key(state, k1)
    state = mix_columns(state)
    state = shift_row(state)
    state = sub_nibbles_inverse(state)
    state = add_round_key(state, k0)

    return state

# Example usage:
ciphertext = 0XC446  # Example 16-bit ciphertext


decrypted_text = mini_aes_decrypt(ciphertext, K0, K1, K2)
print(f"Ciphertext: {bin(ciphertext)}")
print(f"Decrypted Text: {bin(decrypted_text)}")



state = add_round_key(PLAINTEXT, K0)
print_matrix("After AddRoundKey (K0)", state)

state = sub_nibbles(state)
print_matrix("After SubNibbles", state)

state = shift_row(state)
print_matrix("After ShiftRow", state)

state = mix_columns(state)
print_matrix("After MixColumns", state)

state = add_round_key(state, K1)
print_matrix("After AddRoundKey (K1)", state)

state = sub_nibbles(state)
print_matrix("After Final SubNibbles", state)

state = shift_row(state)
print_matrix("After Final ShiftRow", state)

state = add_round_key(state, K2)
print_matrix("Final Ciphertext", state)