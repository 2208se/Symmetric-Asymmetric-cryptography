# Permutation tables
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]

def permute(block, table):
    return [block[i-1] for i in table]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_keys(key):
    # Apply P10 permutation
    key = permute(key, P10)
    
    # Split into left and right halves
    left = key[:5]
    right = key[5:]
    
    # Left shift both halves by 1
    left = left_shift(left, 1)
    right = left_shift(right, 1)
    
    # Combine and apply P8 to get K1
    combined = left + right
    K1 = permute(combined, P8)
    
    # Left shift both halves by 2
    left = left_shift(left, 2)
    right = left_shift(right, 2)
    
    # Combine and apply P8 to get K2
    combined = left + right
    K2 = permute(combined, P8)
    
    return K1, K2

# Example usage
key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
K1, K2 = generate_keys(key)
print("K1:", K1)
print("K2:", K2)