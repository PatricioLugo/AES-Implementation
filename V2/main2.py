from add_round_key2 import add_round_key
from expand_key2 import key_expansion
from sub_bytes2 import sub_bytes
from shift_rows2 import shift_rows
from mix_columns2 import mix_columns

#from inverse_sub_bytes2 import inverse_subbytes
#from inverse_shift_rows2 import inv_shiftrows
#from inverse_mix_columns2 import inverse_mixcolumns
import numpy as np



## Función para leer el archivo
#Retorna 2D numpy array de bloques de 16 bytes en formato entero.
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
    return np.array([np.frombuffer(bytes(b), dtype=np.uint8) for b in unciphered_blocks], dtype=np.uint8)
    
#Función para pedir la Key
def ask_for_key():
    key = np.zeros(16, dtype=np.uint8)
    for i in range(16):
        while True:
            try:
                byte = input(f"Ingresa el byte #{i + 1} de la clave (en hex, por ejemplo '2b'): ")
                key[i] = int(byte, 16)
                break
            except ValueError:
                print("El byte debe ser un número hexadecimal válido (por ejemplo: 2b).")
    return key

#Función para exportar un archivo .aes
def write_ciphered_blocks(ciphered_data, filename): 
    with open(filename, "wb") as f: 
        f.write(ciphered_data)
    print(f'Datos cifrados escritos al archivo {filename}.')

#Función para cifrar un bloque
def cipher_block(input_bytes, expanded_key):
    state = input_bytes
    state = add_round_key(state, expanded_key[0:4])
    for i in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state, i)
        state = mix_columns(state)
        state = add_round_key(state, expanded_key[i*4:(i+1)*4])
    
    state = sub_bytes(state)
    state = shift_rows(state, 10)
    state = add_round_key(state, expanded_key[40:44])
    return state

#Función para hacer XOR entre dos bloques de 16 bytes
def matrix_xor(a, b):
    if a.shape != b.shape:
        print("Matrices must have the same dimensions for XOR operation.")
        return None
    return np.bitwise_xor(a, b)

#Función para cifrar en modo CBC
def cipher(input_bytes, expanded_key):
    ciphered_blocks = []
    i_vec = np.zeros(16, dtype = np.uint8)
    previous_block = i_vec
    for block in input_bytes:
        xored_block = matrix_xor(block, previous_block)
        encrypted_block = cipher_block(xored_block, expanded_key)
        ciphered_blocks.append(encrypted_block)
        previous_block = encrypted_block
    return b"".join(block.tobytes() for block in ciphered_blocks)
#Función para descifrar un bloque

#Función para descifrar en modo CBC

#Función main
def main():
    while True:
        try:
            selection = int(input('1 para cifrado, 2 para descifrado: '))#Input en integer
            match selection:
                case 1: 
                    filename = input('\nDame el nombre del archivo a cifrar: ') #filename en string
                    key = ask_for_key() #Lista de ints
                    expanded_key = key_expansion(key) #Matriz de Keys (c/elemento es int)
                    result = cipher(read_file(filename), expanded_key)
                    write_ciphered_blocks(result, 'output.aes')
                    break  
                case 2:
                   
                    break
                case _:
                    print("Opción no válida.")
        except ValueError:
            print("Por favor ingresa un número válido (1 o 2).")
                


main()