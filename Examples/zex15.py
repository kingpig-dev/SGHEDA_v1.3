def caesar_encrypt(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        # Encrypt uppercase letters
        if char.isupper():
            encrypted_char = chr((ord(char) - 65 + shift) % 26 + 65)
        # Encrypt lowercase letters
        elif char.islower():
            encrypted_char = chr((ord(char) - 97 + shift) % 26 + 97)
        # digit
        elif char.isdigit():
            encrypted_char = chr((ord(char) - 48 + shift) % 10 + 48)
        else:
            # Leave non-alphabetic characters unchanged
            encrypted_char = char
        # print("char: ", char, "encrypted char: ", encrypted_char)
        ciphertext += encrypted_char
    return ciphertext

def caesar_decrypt(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        # Decrypt uppercase letters
        if char.isupper():
            decrypted_char = chr((ord(char) - 65 - shift) % 26 + 65)
        # Decrypt lowercase letters
        elif char.islower():
            decrypted_char = chr((ord(char) - 97 - shift) % 26 + 97)
        elif char.isdigit():
            decrypted_char = chr((ord(char) - 48 - shift) % 10 + 48)
        else:
            # Leave non-alphabetic characters unchanged
            decrypted_char = char
        plaintext += decrypted_char
    return plaintext

# Example usage
plaintext = "4d2a8b152f9172d6"

num_design = '{:4d}'.format(45).replace(' ', '0')
num_analysis = '{:4d}'.format(34).replace(' ', '0')
data = num_design + plaintext[8:16] + num_analysis + plaintext[0:8]
shift = 3



encrypted_text = caesar_encrypt(data, shift)
print("plaintext:", plaintext)
print("Encrypted Text:", encrypted_text)

decrypted_text = caesar_decrypt(encrypted_text, shift)
print("Decrypted Text:", decrypted_text)