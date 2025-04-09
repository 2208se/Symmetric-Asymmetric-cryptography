from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
from Crypto.Hash import SHA256

# Key Generation
def generate_keys(bit_length=1024):
    # Generate two large primes p and q
    p = getPrime(bit_length)
    q = getPrime(bit_length)
    
    # Compute n and phi
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = 65537  # Common choice for e
    while True:
        if gcd(e, phi) == 1:
            break
        e += 2
    
    # Compute d, the modular inverse of e
    d = inverse(e, phi)
    
    # Public key is (n, e), private key is d
    return (n, e), d

# GCD function for choosing e
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Modular Exponentiation
def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

# Encryption
def encrypt(message, public_key):
    n, e = public_key
    m = bytes_to_long(message.encode())
    c = mod_exp(m, e, n)
    return c

# Decryption
def decrypt(ciphertext, private_key, n):
    m = mod_exp(ciphertext, private_key, n)
    message = long_to_bytes(m).decode()
    return message

# Signature Generation
def sign(message, private_key, n):
    # Hash the message
    hash_obj = SHA256.new(message.encode())
    hash_int = bytes_to_long(hash_obj.digest())
    
    # Encrypt the hash with the private key
    signature = mod_exp(hash_int, private_key, n)
    return signature

# Signature Verification
def verify(message, signature, public_key):
    n, e = public_key
    # Decrypt the signature with the public key
    hash_int = mod_exp(signature, e, n)
    
    # Hash the original message
    hash_obj = SHA256.new(message.encode())
    original_hash_int = bytes_to_long(hash_obj.digest())
    
    # Compare the hashes
    return hash_int == original_hash_int

# Example usage
if __name__ == "__main__":
    # Generate keys
    public_key, private_key = generate_keys()
    n, e = public_key
    
    # Message to encrypt
    message = "Chiffrement RSA!"
    
    # Encrypt the message
    ciphertext = encrypt(message, public_key)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt the message
    decrypted_message = decrypt(ciphertext, private_key, n)
    print(f"Decrypted message: {decrypted_message}")
    
    # Generate a signature
    signature = sign(message, private_key, n)
    print(f"Signature: {signature}")
    
    # Verify the signature
    is_valid = verify(message, signature, public_key)
    print(f"Signature valid: {is_valid}")