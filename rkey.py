import random
import string

def generate_key(length=24):
    #generate a random key with uppercase, lowercase, digits, and special characters
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    key = generate_key()
    print(f"Generated Key: {key}")
