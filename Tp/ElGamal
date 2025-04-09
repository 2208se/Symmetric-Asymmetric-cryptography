import random
from Crypto.Hash import SHA256
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

# Key Generation
def generate_keys(bit_length=1024):
    p = get_prime(bit_length)
    g = find_generator(p)
    x = random.randint(1, p-2)
    y = pow(g, x, p)
    return (p, g, y), x

# Encryption
def encrypt(message, public_key):
    p, g, y = public_key
    m = bytes_to_long(message.encode())
    k = random.randint(1, p-2)
    c1 = pow(g, k, p)
    c2 = (m * pow(y, k, p)) % p
    return (c1, c2)

# Decryption
def decrypt(ciphertext, private_key, p):
    c1, c2 = ciphertext
    x = private_key
    s = pow(c1, x, p)
    m = (c2 * inverse(s, p)) % p
    return long_to_bytes(m).decode()

# Signature Generation
def sign(message, private_key, p, g):
    x = private_key
    k = random.randint(1, p-2)
    while gcd(k, p-1) != 1:
        k = random.randint(1, p-2)
    r = pow(g, k, p)
    hash_obj = SHA256.new(message.encode())
    h = bytes_to_long(hash_obj.digest())
    s = (h - x * r) * inverse(k, p-1) % (p-1)
    return (r, s)

# Signature Verification
def verify(message, signature, public_key):
    p, g, y = public_key
    r, s = signature
    hash_obj = SHA256.new(message.encode())
    h = bytes_to_long(hash_obj.digest())
    v1 = pow(g, h, p)
    v2 = (pow(y, r, p) * pow(r, s, p)) % p
    return v1 == v2

# Helper functions
def get_prime(bit_length):
    return getPrime(bit_length)

def find_generator(p):
    for g in range(2, p):
        if pow(g, (p-1)//2, p) != 1 and pow(g, p-1, p) == 1:
            return g
    return None

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def inverse(a, m):
    return pow(a, -1, m)

def bytes_to_long(b):
    return int.from_bytes(b, 'big')

def long_to_bytes(l):
    return l.to_bytes((l.bit_length() + 7) // 8, 'big')

# Example usage
if __name__ == "__main__":
    # Generate keys
    public_key, private_key = generate_keys()
    p, g, y = public_key
    
    # Message to encrypt
    message = "Chiffrement ElGamal!"
    
    # Encrypt the message
    ciphertext = encrypt(message, public_key)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt the message
    decrypted_message = decrypt(ciphertext, private_key, p)
    print(f"Decrypted message: {decrypted_message}")
    
    # Generate a signature
    signature = sign(message, private_key, p, g)
    print(f"Signature: {signature}")
    
    # Verify the signature
    is_valid = verify(message, signature, public_key)
    print(f"Signature valid: {is_valid}")