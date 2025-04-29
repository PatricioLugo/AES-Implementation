from add_round_key import add_round_key_func
from expand_key import expand_key_func
from sub_bytes import subbytes
from inverse_sub_bytes import inverse_subbytes
from shift_rows import shiftrows
from inverse_shift_rows import inv_shiftrows
from mix_columns import mix_columns
from inverse_mix_columns import inverse_mixcolumns

def write_ciphered_blocks(blocks, filename):
    with open(filename, 'wb') as file:
        for block in blocks:
            for row in block:
                for byte_str in row:
                    byte_value = int(byte_str, 16)
                    file.write(byte_value.to_bytes(1, 'big'))

def cipher_block(input_bytes, expanded_key):
    state = input_bytes
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

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def cipher(input_bytes, expanded_key):
    unciphered_blocks = input_bytes
    ciphered_blocks = []
    i_vec = bytes([0]*16)
    previous_block = i_vec
    for block in unciphered_blocks:
        xored_block = xor_bytes(block, previous_block)
        encrypted_block = cipher_block(xored_block, expanded_key)
        ciphered_blocks.append(encrypted_block)
        previous_block = encrypted_block
    return b"".join(ciphered_blocks)

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

example = [[0x32, 0x88, 0x31, 0xe0], 
           [0x43, 0x5a, 0x31, 0x37], 
           [0xf6, 0x30, 0x98, 0x07],
           [0xa8, 0x8d, 0xa2, 0x34]]

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
                result = cipher(example, expanded_key) #read_file(filename)
                write_ciphered_blocks(result, "output.aes")
                
            case 2:
                filename = input('\nDame el nombre del archivo a descifrar: ')
                # Llamada a función de descifrado
            case _:
                print("ERROR: Ingresa un número válido.")   

main()