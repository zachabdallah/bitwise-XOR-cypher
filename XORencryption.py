from rkey import generate_key
from rkey import passphrase_key
CONTROL_CHAR_NAMES = {#dictionary generated with chatGPT
    0: "NUL", 1: "SOH", 2: "STX", 3: "ETX", 4: "EOT", 5: "ENQ", 6: "ACK", 7: "BEL", 8: "BS", 9: "TAB", 10: "LF", 11: "VT", 12: "FF", 13: "CR", 14: "SO",
    15: "SI", 16: "DLE", 17: "DC1", 18: "DC2", 19: "DC3", 20: "DC4", 21: "NAK", 22: "SYN", 23: "ETB", 24: "CAN", 25: "EM", 26: "SUB", 27: "ESC", 28: "FS", 29: "GS",
    30: "RS", 31: "US", 32: "SPACE", 33: "!", 34: "\"", 35: "#", 36: "$", 37: "%", 38: "&", 39: "'", 40: "(", 41: ")", 42: "*", 43: "+", 44: ",",
    45: "-", 46: ".", 47: "/", 48: "0", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6", 55: "7", 56: "8", 57: "9", 58: ":", 59: ";",
    60: "<", 61: "=", 62: ">", 63: "?", 64: "@", 65: "A", 66: "B", 67: "C", 68: "D", 69: "E",  70: "F", 71: "G", 72: "H", 73: "I", 74: "J",
    75: "K", 76: "L", 77: "M", 78: "N", 79: "O", 80: "P", 81: "Q", 82: "R", 83: "S", 84: "T", 85: "U", 86: "V", 87: "W", 88: "X", 89: "Y",
    90: "Z", 91: "[", 92: "\\", 93: "]", 94: "^",  95: "_", 96: "`", 97: "a", 98: "b", 99: "c", 100: "d", 101: "e", 102: "f", 103: "g", 104: "h",
    105: "i", 106: "j", 107: "k", 108: "l", 109: "m", 110: "n", 111: "o", 112: "p", 113: "q", 114: "r", 115: "s", 116: "t", 117: "u", 118: "v", 119: "w",
    120: "x", 121: "y", 122: "z", 123: "{", 124: "|", 125: "}", 126: "~", 127: "DEL"
}

##################################################################################################################################################

def print_ASCII(plaintext, encrypted_text, key):
    print(f"{'Char       ASCII         Key    Key ASCII    XOR Result '}")
    print("=" * 60)   

    i = 0
    for p, k in zip(plaintext, key * (len(plaintext) // len(key) + 1)):
        x = CONTROL_CHAR_NAMES.get(ord(encrypted_text[i]), encrypted_text[i])#for some reason i needed two arguments here, the second being that if there was an error retrieving from the dictionary, .get() would simply return encrypted_text[i] which would keep the original text and not throw a weird error. I guess the compiler is just trying to not cause issues.
        xor_result = ord(p) ^ ord(k)
        print_xor_result = CONTROL_CHAR_NAMES.get(xor_result)
        print(f"{p:<1} -> {x:<6}{ord(p):3} -> {ord(encrypted_text[i]):<7}{k:<7}{ord(k):<13}{xor_result:<3}: {print_xor_result}")
        i += 1
        #alright so this function is just making it easyto see what ASCII values are actually being compared. The key ASCII and the original ASCII values are being compared character by character, and the output of this bitwise XOR operation is a new ASCII value (that might be converted to a character, but might also not be printable), and then all those characters are concatenated to become the decrypted string

##################################################################################################################################################

def printable_xor_output(text): #this is only a print function, we aren't replacing original values
    return "".join(
        CONTROL_CHAR_NAMES.get(ord(c), c) for c in text
    )

##################################################################################################################################################

def xor_encrypt(plaintext, key):
    encrypted = [chr(ord(p) ^ ord(k)) for p, k in zip(plaintext, key * (len(plaintext) // len(key) + 1))]
    #this is called list comprehension. 
    #ord() converts character to ASCII (p for plaintext, k for key)
    # ^ is a XOR operator, which applies a bitwise XOR. 
    #chr() converts that result back into a character

    #for the second part, zip() pairs each character in plaintext with a character from the repeated key
    #(key * (len(plaintext) // len(key) + 1) repeats the key enough times to cover the length of the plaintext (// is a floor() function btw)
    #so essentially, it goes through each pair (p,k), XORS them, converts them back into a character, amd then stores them into a list called "encyrpted"

    return "".join(encrypted)#convert the list to a string

##################################################################################################################################################

def xor_decrypt(ciphertext, key):
    decrypted = [chr(ord(c) ^ ord(k)) for c, k in zip(ciphertext, key * (len(ciphertext) // len(key) + 1))]
    return "".join(decrypted)

##################################################################################################################################################

message = "hello my name is zach"
#key = generate_key(10)  # we should think about how to privatize this key or have a way to generate it so that it's not easily guessable or brute-forced
passphrase = "superstrongpassphrase" #using your own passphrase to generate key (more convenient for users)
key = passphrase_key(passphrase)
print(f"Generated Key: {key}") #This is a mark for me to come back to. See comment below(Jarret)

########################################################################################################################################################################

#Julian made a good point with the key generation for ease of use for the users.
#But what what happens if one of these user passphrase ends up get comprimised.
#I think we should add a timer and or a limited attempt passphrase function.
#This might be redundant on the way the key is generated, but it's a good idea to have a backup plan.

'''
Jarrett has a good idea, but we should have multiple keys to guess, 
all with varying levels of defense. An example would be a repeating 
key, a long key like we currently have, and a randomly generated key.
This way, as the attacker, we can show the importance of creating a 
meaningful defense.

'''                               

##################################################################################################################################################

encrypted_text = xor_encrypt(message, key)
print_ASCII(message, encrypted_text, key)
decrypted_text = xor_decrypt(encrypted_text, key)

print(f"\nOriginal message: {message}")
print(f"Key: {key}")
print(f"Encrypted message: {printable_xor_output(encrypted_text)}")
print(f"How the message would appear without converting ASCII values: {encrypted_text}")
print(f"Decrypted: {decrypted_text}")

##################################################################################################################################################

'''example:

plaintext = "HELLO"
key = "KEY"
len(plaintext) = 5
len(key) = 3
KEY * (5//3 + 1) = KEY * (floor(1.67) + 1) = KEY * 2 = "KEYKEY"

pair using zip():
H E L L O
K E Y K E

Plaintext -> (ASCII)	Key (ASCII)	     XOR Result
H -> (72)	            K -> (75)	     3
E -> (69)	            E -> (69)	     0
L -> (76)	            Y -> (89)	     21
L -> (76)	            K -> (75)	     7
O -> (79)	            E -> (69)	     10

output is now {char(3), char(0), char(21), char(7), char(10)}, though many of these characters are not printable

after joining, the message is currently a string of weird, possibly non-printable characters that we concatenated back together.


note: keep in mind that a bitwise XOR operation is comparing the bits of two binary numbers and returning 0 or 1 per each bit. example:  0101 
                        0011
                result: 0110 
        so it returns 0 if the compared bits are the same, and 1 otherwise. In this case, 5 ^ 3 = 6
'''