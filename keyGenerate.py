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
