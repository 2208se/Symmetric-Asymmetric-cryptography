import hmac
import hashlib
import binascii

def hmac_sha1_manual(key_hex, message_hex):
   
    block_size = 64
    ipad = 0x36
    opad = 0x5C
    
    # Convert hex strings to bytes
    key = binascii.unhexlify(key_hex.replace("x", ""))
    message = binascii.unhexlify(message_hex.replace("x", ""))
    
    print(f"Original key (hex): {key_hex} → Bytes: {binascii.hexlify(key).decode()}")
    print(f"Original message (hex): {message_hex} → Bytes: {binascii.hexlify(message).decode()}")

    # Step 1: Prepare K₀
    if len(key) > block_size:
        key = hashlib.sha1(key).digest()
        print(f"Key hashed (SHA-1) since it was longer than block size: {binascii.hexlify(key).decode()}")
    key_bytes = key + bytes([0] * (block_size - len(key)))
    print(f"K₀ : {binascii.hexlify(key_bytes).decode()}")

    # Step 2: K₀ XOR ipad ()
    xor_ipad = bytes([b ^ ipad for b in key_bytes])
    print(f"K₀ XOR ipad: {binascii.hexlify(xor_ipad).decode()}")

    # Step 3: (K₀ XOR ipad) || message    step 2+ ipad 
    inner_message = xor_ipad + message
    print(f"Inner message (K₀ XOR ipad || message): {binascii.hexlify(inner_message).decode()}")

    # Step 4: First hash
    hash1 = hashlib.sha1(inner_message).digest()
    print(f"SHA1(inner message): {binascii.hexlify(hash1).decode()}")

    # Step 5: K₀ XOR opad
    xor_opad = bytes([b ^ opad for b in key_bytes])
    print(f"K₀ XOR opad: {binascii.hexlify(xor_opad).decode()}")

    # Step 6: (K₀ XOR opad) || hash1  step 4+step5
    outer_message = xor_opad + hash1
    print(f"Outer message (K₀ XOR opad || hash1): {binascii.hexlify(outer_message).decode()}")

    # Step 7: Final hash ofeverything 
    hmac_result = hashlib.sha1(outer_message).digest()
    print(f"Final HMAC-SHA1: {binascii.hexlify(hmac_result).decode()}\n")
    
    return hmac_result

# Given values (hex strings)
key_hex = "x466666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666B6579"       # "Key" in ASCII 
message_hex = "x48656C6C6F" # "Hello" in ASCII 

# Manual implementation
manual_hmac = hmac_sha1_manual(key_hex, message_hex)
print("Manual HMAC-SHA1:", binascii.hexlify(manual_hmac).decode())

# Verification with Python's hmac
correct_hmac = hmac.new(
    binascii.unhexlify(key_hex.replace("x", "")),
    binascii.unhexlify(message_hex.replace("x", "")),
    hashlib.sha1
).digest()
print("Built-in HMAC-SHA1:", binascii.hexlify(correct_hmac).decode())

# Verify
assert manual_hmac == correct_hmac, "Implementation doesn't match!"
print("Verification successful!")