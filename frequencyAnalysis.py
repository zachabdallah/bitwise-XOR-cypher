import random
import string

# passages provided by Chat GPT
def generate_paragraph():
    passages = [
        # Excerpt from "Pride and Prejudice" by Jane Austen
        """It is a truth universally acknowledged, that a single man in possession of a good fortune, 
must be in want of a wife. However little known the feelings or views of such a man may be on 
his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, 
that he is considered as the rightful property of some one or other of their daughters. 
“My dear Mr. Bennet,” said his lady to him one day, “have you heard that Netherfield Park is let at last?”""",

        # Excerpt from "Moby Dick" by Herman Melville
        """Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, 
and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. 
It is a way I have of driving off the spleen and regulating the circulation. Whenever I find myself growing grim about the mouth; 
whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, 
and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, 
that it requires a strong moral principle to prevent me from deliberately stepping into the street, 
and methodically knocking people’s hats off—then, I account it high time to get to sea as soon as I can.""",

        # Excerpt from "Alice's Adventures in Wonderland" by Lewis Carroll
        """Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: 
once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 
'and what is the use of a book,' thought Alice 'without pictures or conversation?' So she was considering in her own mind 
(as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain 
would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.""",

        # Excerpt from "The Adventures of Sherlock Holmes" by Arthur Conan Doyle
        """To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any other name. 
In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler. 
All emotions, and that one particularly, were abhorrent to his cold, precise but admirably balanced mind. 
He was, I take it, the most perfect reasoning and observing machine that the world has seen, but as a lover he would have placed himself 
in a false position. He never spoke of the softer passions, save with a gibe and a sneer.""",

        # Excerpt from "The War of the Worlds" by H.G. Wells
        """No one would have believed in the last years of the nineteenth century that this world was being watched keenly and closely 
by intelligences greater than man’s and yet as mortal as his own; that as men busied themselves about their various concerns 
they were scrutinized and studied, perhaps almost as narrowly as a man with a microscope might scrutinize the transient creatures 
that swarm and multiply in a drop of water. With infinite complacency men went to and fro over this globe about their little affairs, 
serene in their assurance of their empire over matter. It is possible that the infusoria under the microscope do the same.""",

        # Excerpt from "The Hobbit" by J.R.R. Tolkien
        """In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, 
nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort. 
It had a perfectly round door like a porthole, painted green, with a shiny yellow brass knob in the exact middle. 
The door opened on to a tube-shaped hall like a tunnel: a very comfortable tunnel without smoke, with panelled walls, 
and floors tiled and carpeted, provided with polished chairs, and lots and lots of pegs for hats and coats - the hobbit 
was fond of visitors."""
    ]

    return random.choice(passages)


# Generates a 1:1 letter substitution based on the key.
def generate_cipher_mapping(key):
    alphabet = list(string.ascii_lowercase)  # Create a list of lowercase letters
    shuffled_alphabet = list(alphabet)
    random.seed(key)  # Seed random shuffling for consistent mapping
    random.shuffle(shuffled_alphabet)  # Shuffle letters to create a substitution cipher
    
    # Create mapping dictionaries
    encrypt_mapping = {plaintext: cipher for plaintext, cipher in zip(alphabet, shuffled_alphabet)}
    decrypt_mapping = {cipher: plaintext for plaintext, cipher in zip(alphabet, shuffled_alphabet)}
    
    return encrypt_mapping, decrypt_mapping


# Encrypts using a 1:1 substitution cipher instead of XOR/
def xor_encrypt(plaintext, key):
    encrypt_mapping, _ = generate_cipher_mapping(key)  # Get encryption mapping
    ciphertext = []
    
    for char in plaintext:
        if char.lower() in encrypt_mapping:  # Encrypt letters only
            encrypted_char = encrypt_mapping[char.lower()]
            ciphertext.append(encrypted_char.upper() if char.isupper() else encrypted_char)
        else:
            ciphertext.append(char)  # Preserve non-letters (spaces, punctuation)
    
    return ''.join(ciphertext)

# Decrypts using the predefined 1:1 substitution cipher.
def xor_decrypt(ciphertext, key):
    _, decrypt_mapping = generate_cipher_mapping(key)  # Get decryption mapping
    decrypted_text = []
    
    for char in ciphertext:
        if char.lower() in decrypt_mapping:  # Decrypt only if it's a letter
            decrypted_char = decrypt_mapping[char.lower()]
            decrypted_text.append(decrypted_char.upper() if char.isupper() else decrypted_char)
        else:
            decrypted_text.append(char)  # Preserve punctuation/spaces
    
    return ''.join(decrypted_text)


# Performs frequency analysis on ciphertext.
def frequency_analysis(ciphertext):
    frequencies = {}
    for char in ciphertext.lower():
        if 'a' <= char <= 'z':
            frequencies[char] = frequencies.get(char, 0) + 1
    total_letters = sum(frequencies.values())
    percentages = {char: (count / total_letters) * 100 for char, count in frequencies.items()}
    sorted_percentages = dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))
    return sorted_percentages


# Decrypts ciphertext based on user guesses.
def decrypt_with_guesses(ciphertext, guesses):
    decrypted_text = []
    for char in ciphertext:
        if 'a' <= char.lower() <= 'z':
            decrypted_char = guesses.get(char.lower(), '_')
            decrypted_text.append(decrypted_char.upper() if char.isupper() else decrypted_char)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)


# Main function for encryption and decryption.
def main():
    plaintext = generate_paragraph()
    key = ''.join(random.choices(string.ascii_letters, k=10))  # Generates a random 10-character key

    ciphertext = xor_encrypt(plaintext, key)

    guesses = {}
    decrypted_text = decrypt_with_guesses(ciphertext, guesses)

    # print(f"")
    # print(f"Generated Key:", key)  # Show the generated key

    while "_" in decrypted_text:
        # Always reprint the encrypted message
        print()
        print(f"Encrypted Message:")
        print(ciphertext)  

        print()
        print(f"Decrypted Message (Updated):")
        print(decrypted_text)

        # Frequency Analysis
        frequencies = frequency_analysis(ciphertext)
        print()
        print(f"Frequency Analysis:")
        for char, percentage in frequencies.items():
            print(f"{char}: {percentage:.2f}%")

        # Show Used Characters
        used_chars_display = ", ".join(f"{c} -> {guesses.get(c, '')}" for c in sorted(guesses))
        print(f"\nAlready used: {used_chars_display if used_chars_display else 'None'}")

        # Get User Input
        guess_input = input("\nEnter a ciphertext character and its plaintext guess (e.g., 'x, e') or 'quit' to exit: ").lower()
        if guess_input == 'quit':
            break

        try:
            ciphertext_char, plaintext_char = map(str.strip, guess_input.split(","))
            if len(ciphertext_char) != 1 or len(plaintext_char) != 1 or not ('a' <= ciphertext_char <= 'z') or not ('a' <= plaintext_char <= 'z'):
                print(f"Invalid input. Please use the format 'x, e'.")
                continue

            if ciphertext_char not in ciphertext.lower():
                print(f"The letter you entered is not in the encrypted message.")
                continue

            guesses[ciphertext_char] = plaintext_char
            decrypted_text = decrypt_with_guesses(ciphertext, guesses)

        except ValueError:
            print(f"Invalid input format. Please use the format 'x, e'.")

    if "_" not in decrypted_text:
        print()
        print(f"Decryption Complete!")
        print(f"Final Decrypted Message:")
        print(decrypted_text)

if __name__ == "__main__":
    main()