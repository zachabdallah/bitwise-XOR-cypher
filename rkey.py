import secrets
import string
import hashlib
import base64

#simpler random key generation
def generate_key(length=24):
    #generate a random key with uppercase, lowercase, digits, and special characters
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

if __name__ == "__main__":
    key = generate_key()
    print(f"Generated Key: {key}")

#key generation with passphrase
def passphrase_key(passphrase, salt=None, iterations=100_000, dklen=10):

    """
    Derives a key from a passphrase using PBKDF2 (HMAC-SHA256). kdf = key derivation function
    Salt is a randomly generated string that is appened or prepended to the passphrase before KDF.
    ^ this ensures that each user/item needs a separate brute force attempt, this prevents large scale precomputation attacks
    """

    if salt is None:
        #generate a new random salt (16 bytes, higher = better)
        salt = secrets.token_bytes(16)
    
    #PBKDF2 with HMAC-SHA256
    key = hashlib.pbkdf2_hmac(
        'sha256', 
        passphrase.encode('utf-8'), salt, iterations, dklen=dklen
    )
    
    #combine salt + derived key in one string
    return base64.urlsafe_b64encode(salt + key).decode('utf-8')

if __name__ == "__main__":
    passphrase = "superstrongpassphrase"  #passphrase
    derived_key = passphrase_key(passphrase)
    print(f"Derived Key (Salt + Key): {derived_key}")