import random
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

# Key Generation
def generate_keys(bit_length=1024):
    # Generate two large primes p and q such that p ≡ 3 mod 4 and q ≡ 3 mod 4
    p = getPrime(bit_length)
    while p % 4 != 3:
        p = getPrime(bit_length)
    
    q = getPrime(bit_length)
    while q % 4 != 3:
        q = getPrime(bit_length)
    
    # Compute n = p * q
    n = p * q
    # Public key is n, private key is (p, q)
    return n, (p, q)

# Encryption
def encrypt(message, public_key):
    n = public_key
    m = bytes_to_long(message.encode())
    c = pow(m, 2, n)  # c = m^2 mod n
    return c

# Decryption
def decrypt(ciphertext, private_key):
    p, q = private_key
    n = p * q
    # Compute square roots modulo p and q
    mp = pow(ciphertext, (p + 1) // 4, p)
    mq = pow(ciphertext, (q + 1) // 4, q)
    
    # Use the Chinese Remainder Theorem to find the four possible roots
    yp = inverse(p, q)
    yq = inverse(q, p)
    
    r1 = (yp * p * mq + yq * q * mp) % n
    r2 = n - r1
    r3 = (yp * p * mq - yq * q * mp) % n
    r4 = n - r3
    
    # Return all four possible roots
    return [long_to_bytes(r) for r in [r1, r2, r3, r4]]

# Example usage
if __name__ == "__main__":
    # Generate keys
    public_key, private_key = generate_keys()
    n = public_key
    p, q = private_key
    
    # Message to encrypt
    message = "Chiffrement Rabin!"
    print(f"Original message: {message}")
    
    # Encrypt the message
    ciphertext = encrypt(message, n)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt the message
    possible_messages = decrypt(ciphertext, (p, q))
    print("Possible decrypted messages:")
    
    # Filter out invalid messages
    valid_messages = []
    for msg in possible_messages:
        try:
            # Try to decode the message
            decoded_msg = msg.decode('utf-8')
            valid_messages.append(decoded_msg)
        except UnicodeDecodeError:
            # Skip invalid messages
            continue
    
    # Display valid messages
    for i, msg in enumerate(valid_messages):
        print(f"Option {i + 1}: {msg}")
