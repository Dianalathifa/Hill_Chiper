#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import string
import random
from sympy import Matrix

def input_key_matrix(dimension):
    key = []
    print("Masukkan nilai-nilai untuk matriks kunci:")
    for i in range(dimension):
        row = []
        for j in range(dimension):
            while True:
                try:
                    value = int(input(f"Masukkan nilai untuk baris {i + 1}, kolom {j + 1}: "))
                    break
                except ValueError:
                    print("Input invalid. Masukkan nilai dalam bentuk angka.")
            row.append(value)
        key.append(row)
    return key

def encrypt(plaintext, key):
    dimension = len(key)
    alphabet = string.ascii_uppercase
    encrypted_message = ""
    plaintext = plaintext.upper()

    plaintext = ''.join(char for char in plaintext if char in alphabet)

    padding_length = (dimension - (len(plaintext) % dimension)) % dimension
    plaintext += ''.join(random.choice(alphabet) for _ in range(padding_length))

    for index in range(0, len(plaintext), dimension):
        values = []

        for j in range(dimension):
            if index + j < len(plaintext):
                values.append([alphabet.index(plaintext[index + j])])

        vector = np.matrix(values)
        result = key * vector % 26

        for j in range(dimension):
            encrypted_message += alphabet[result.item(j)]

    return encrypted_message

def generate_inverse_matrix(key_matrix):
    key = Matrix(key_matrix)
    key_inv = key.inv_mod(26)
    return key_inv

def decrypt(encrypted_message, key_matrix):
    dimension = len(key_matrix)
    alphabet = string.ascii_uppercase
    key_inv = generate_inverse_matrix(key_matrix)

    if key_inv is None:
        return "Matriks kunci dekripsi tidak dapat diinvers."

    key_inv = key_inv.tolist()
    decrypted_message = ""

    for index, char in enumerate(encrypted_message):
        values = []
        if index % dimension == 0:
            for j in range(dimension):
                values.append([alphabet.index(encrypted_message[index + j])])

            vector = np.matrix(values)
            result = key_inv * vector % 26

            for j in range(dimension):
                decrypted_message += alphabet[result.item(j)].lower()

    return decrypted_message

if __name__ == "__main__":
    dimension = int(input("Masukkan dimensi matriks kunci untuk enkripsi: "))
    key_matrix = input_key_matrix(dimension)

    print("Matriks kunci enkripsi:")
    print(np.matrix(key_matrix))

    plaintext = input("Masukkan teks plainteks: ").upper()
    print("Plaintext:", plaintext)

    encrypted_message = encrypt(plaintext, np.matrix(key_matrix))
    print("Teks Terenkripsi:", encrypted_message)

    decrypt_option = input("Apakah Anda ingin mendekripsi teks? (Y/N): ").upper()

    if decrypt_option == "Y":
        key_matrix_decrypt = input_key_matrix(dimension)
        decrypted_message = decrypt(encrypted_message, key_matrix_decrypt)
        print("Teks terdekripsi:", decrypted_message)


# In[ ]:




