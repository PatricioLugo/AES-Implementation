from add_round_key import add_round_key_func
from expand_key import expand_key_func
from sub_bytes import subbytes
from inverse_sub_bytes import inverse_subbytes
from shift_rows import shiftrows
from inverse_shift_rows import inv_shiftrows
from mix_columns import mix_columns
from inverse_mix_columns import inverse_mixcolumns
import numpy as np

def write_ciphered_blocks(blocks, filename):
    with open(filename, 'wb') as file:
        for block in blocks:
            for row in block:
                for byte_str in row:
                    byte_value = int(byte_str, 16)
                    file.write(byte_value.to_bytes(1, 'big'))

def cipher_block(input_bytes, expanded_key):
    state = input_bytes
    print(expanded_key)
    state = add_round_key_func(state, expanded_key[0])
    for i in range(1, 9):
        state = subbytes(state)
        state = shiftrows(state)
        state = mix_columns(state)
        state = add_round_key_func(state, expanded_key[i])
    
    state = subbytes(state)
    state = shiftrows(state)
    state = add_round_key_func(state, expanded_key[9])
    return state

def decipher_block(input_bytes, expanded_key):
    state = input_bytes
    state = add_round_key_func(state, expanded_key[9])      # Add round key 10
    for i in range(8, 0, -1):       # Inverse iteration 
        state = inv_shiftrows(state)
        state = inverse_subbytes(state)
        state = add_round_key_func(state, expanded_key[9-i])    
        state = inverse_mixcolumns(state)
    
    state = inv_shiftrows(state)
    state = inverse_subbytes(state)
    state = add_round_key_func(state, expanded_key[0])   #Add round key 1  
    return state


def matrix_xor(a, b):
    a_array = np.array(a)
    b_array = np.array(b)
    if a_array.shape != b_array.shape:
        print("Matrices must have the same dimensions for XOR operation.")
        return None
    return np.bitwise_xor(a_array, b_array)

def cipher(input_bytes, expanded_key):
    unciphered_blocks = input_bytes
    ciphered_blocks = []
    i_vec = [
    [0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00]
]
    previous_block = i_vec
    for block in unciphered_blocks:
        xored_block = matrix_xor(block, previous_block)
        encrypted_block = cipher_block(xored_block.tolist(), expanded_key)
        ciphered_blocks.append(encrypted_block)
        previous_block = encrypted_block
    return b"".join(ciphered_blocks)


def decipher(input_bytes, expanded_key): 
    unciphered_blocks = input_bytes
    deciphered_blocks = []
    i_vec = [
    [0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00]
]
    previous_block = i_vec
    for block in unciphered_blocks:
        decrypted_block = decipher_block(block.tolist(), expanded_key)
        xored_block = matrix_xor(decrypted_block, previous_block)
        deciphered_blocks.append(xored_block)
        previous_block = block
    return b"".join(deciphered_blocks)

def read_file(filename):
    unciphered_blocks = []
    with open(filename, 'rb') as f:
        while True:
            block = f.read(16)
            if not block:
                break
            if len(block) < 16:
                padding_needed = 16 - len(block)
                if padding_needed >= 1:
                    block += bytes([0x01]) + bytes([0x00] * (padding_needed - 1))
            unciphered_blocks.append(block)
    return unciphered_blocks

def ask_for_key():
    key = []
    for i in range(16):
        key_value = input("Ingresa un valor en hexadecimal: ")
        key.append(key_value)
    return key



def main():
    print('Bienvenido al programa de encriptación y decriptación usando AES\n')
    while True:
        print('1. Cifrado')
        print('2. Descifrado')
        selection = int(input('Selecciona la opción deseada: '))
        match selection:
            case 1:
                filename = input('\nDame el nombre del archivo a cifrar: ')
                # LLamada a función de cifrado
                key = ask_for_key()     
                expanded_key = expand_key_func(key)
                result = cipher(read_file(filename), expanded_key) #read_file(filename)
                write_ciphered_blocks(result, "output.aes")
                
            case 2:
                filename = input('\nDame el nombre del archivo a descifrar: ')
                # LLamada a función de descifrado
                key = ask_for_key()
                expanded_key = expand_key_func(key)
                result = decipher(read_file(filename), expanded_key)
                write_ciphered_blocks(result, "output.pdf")
                
            case _:
                print("ERROR: Ingresa un número válido.")   

main()