import numpy as np
import math

# Constants for bases
base_x = 0
base_plus = 1

def generate_random_key(key_length):
    # Generates a random binary key
    return np.random.randint(2, size=key_length)

def generate_random_bases(length):
    # Generates random bases (0 for rectilinear, 1 for diagonal)
    return np.random.randint(2, size=length)

def alice_encoding(key_length, alice_bits, alice_base):
    # Encoding of alice, between the bases with the polarization
    polarization = []
    for i in range(key_length): # polarization encoding
            if alice_base[i] == base_x: # if base is x: polarization is either 45 or -45
                polarization.append(45 if alice_bits[i] == 1 else -45)
            else: # if base is +: polarization is either 90 or 0
                 polarization.append(90 if alice_bits[i] == 1 else 0)
    return polarization

def bob_encoding(key_length, bob_base):
    # Encoding of bob, depending on the base
    polarization = []
    for i in range(key_length):
        if bob_base[i] == base_x: 
            polarization.append(45)
        else:
            polarization.append(0)
    return polarization

def bob_measurement(key_length, alice_encoded, bob_encoded):
    # measurement of bob's bits
    bob_measuring = []
    print("[#] Enter the measured bits from Bob!")
    for i in range(key_length):
        bob_input = input(f"[#] Alice:{str(alice_encoded[i]).rjust(3)}, Bob:{str(bob_encoded[i]).rjust(3)}: ")
        if bob_input == '0' or bob_input == '1':
            bob_measuring.append(bob_input)
        else:
            print("[-] Error: Enter '0' or '1'!")
    return bob_measuring     

def bob_key(key_length ,alice_base, bob_base, bob_measure, alice_bits):
    # matching bases appends bob's bit to the encryption key
    enc_key = []
    error_rate = 0
    bit_rate = 0
    for i in range(key_length):
        if alice_base[i] == bob_base[i]:
            enc_key.append(bob_measure[i])
            bit_rate += 1
            if alice_bits[i] != bob_measure[i]:
                error_rate += 1
    if error_rate > 0:
        error_rate_perc = (1-(error_rate/bit_rate))*100
        if error_rate_perc < 25:
            print(f"[-] Error rate is {error_rate_perc}%")
        else:
            print(f"[-] The error rate is to high with {error_rate_perc}%, the key shouldn't be used!")
            print("[-] The program will exit!")
            exit()
    else:
        print("[+] Error rate is 0%")
    return enc_key

def alice_key_gen(key_length ,alice_base, bob_base, alice_bits):
    alice_key = []
    for i in range(key_length):
        if alice_base[i] == bob_base[i]:
            alice_key.append(alice_bits[i])
    return alice_key

def bb84_protocol(key_length):
    # steps of the BB84 protocol 
    alice_bits = generate_random_key(key_length)
    print("[+] Alice's Bits:", alice_bits)
    alice_base = generate_random_bases(key_length)
    #alice_base = [-45, 0, 45, 90, -45, 0, 45, 90, -45, 0, 45, 90, -45, 0, 45, 90]
    alice_base_to_print = []
    for i in range(len(alice_base)):
        if alice_base[i] == base_plus:
            alice_base_to_print.append("+")
        else:
            alice_base_to_print.append("x")
    print("[+] Alice's Base:", alice_base_to_print)
    alice_encoded = alice_encoding(key_length, alice_bits, alice_base)
    print("[+] Alice polarization", alice_encoded)
    bob_base = generate_random_bases(key_length)
    #bob_base = [-45, 0, 45, 90, -45, 0, 45, 90, -45, 0, 45, 90, -45, 0, 45, 90]
    bob_base_to_print = []
    for i in range(len(bob_base)):
        if bob_base[i] == base_plus:
            bob_base_to_print.append("+")
        else:
            bob_base_to_print.append("x")
    print("[+] Bob's base:", bob_base_to_print)
    bob_encoded = bob_encoding(key_length, bob_base)
    print("[+] Bob polarization:", bob_encoded)
    bob_measure = bob_measurement(key_length, alice_encoded, bob_encoded)
    print("[+] Bob measurement:", bob_measure)
    bob_enc_key = bob_key(key_length, alice_base, bob_base, bob_measure, alice_bits)
    print("[+] Bobs encryption key: ", bob_enc_key)
    return bob_enc_key, alice_base, bob_base, alice_bits

def encrypt(key, word_bin):
    # from string to encrypted binary
    encrypted = []
    print(f"[+] Key len: {len(key)}")
    print("[+] Bin: ", word_bin)
    print(f"[+] Bin len: {len(word_bin)}")
    # check if key length is long enough to encrypt the binary
    if(len(key) < len(word_bin)):
        print("[-] Your key is not sufficiently long to encrypt the word!")
        exit()
    for i in range(len(word_bin)):
        encrypted.append(int(key[i]) ^ int(word_bin[i]))
    return encrypted

def decrypt_bin(encrypted_word, key):
    # from encrypted binary to decrypted string
    decrypted = []
    for i in range(len(encrypted_word)):
        decrypted.append(int(key[i]) ^ int(encrypted_word[i]))
    decrypted_bin = ''.join(str(x) for x in decrypted)
    return ''.join(chr(int(decrypted_bin[i*8:i*8+8],2)) for i in range(len(decrypted_bin)//8))

def decrypt_bin_to_word(encrypted_word):
    # from encrypted binary to string
    word = []
    word = ''.join(str(x) for x in encrypted_word)
    return ''.join(chr(int(word[i*8:i*8+8],2)) for i in range(len(word)//8))


if __name__ == "__main__":
    #print("[#] --- BB84 PROTOCOL TESTING! ---")
    #print("[#] ---     CHANGE BASES!      ---")
    word = input("[#] Enter the word to encrypt: ")
    print("[+] Entered word: ", word)
    print("[+] Len of entered word: ", len(word))

    buffer = input("[#] Enter the buffer in %: ")
    error_rate = input("[#] Enter the error rate in %: ")
    multiplier = 2 * (1+(float(buffer)/100)) * (1+(float(error_rate)/100))
    print("[+] Multiplier: ", multiplier)


    word_bin = ''.join(format(ord(i), '08b') for i in word)
    print("[+] Word binary: ", word_bin)
    print("[+] Len of word binary: ", len(word_bin))

    key_length = math.ceil((int(len(word_bin))* multiplier))
    print("[+] Key length: ", key_length)
    bobs_result, alice_base, bob_base, alice_bits = bb84_protocol(key_length)

    encrypted_bin = encrypt(bobs_result, word_bin)
    print("[+] Encrypted binary: ", encrypted_bin)

    encrypted_word = decrypt_bin_to_word(encrypted_bin)
    print("[+] Encrypted word: ", encrypted_word)

    # decrypt with alices key
    alices_result = alice_key_gen(key_length, alice_base, bob_base, alice_bits)
    print("[+] Alices encryption key: ", alices_result)

    decrypted_word = decrypt_bin(encrypted_bin, alices_result)
    print("[+] Decrypted word: ", decrypted_word)
    exit()
