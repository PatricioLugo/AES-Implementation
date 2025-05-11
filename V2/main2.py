from add_round_key2 import add_round_key
from expand_key2 import key_expansion
from sub_bytes2 import sub_bytes
from shift_rows2 import shift_rows
from mix_columns2 import mix_columns

from inverse_sub_bytes2 import inv_subbytes
from inverse_shift_rows2 import inv_shiftrows
from inverse_mix_columns2 import inverse_mixcolumns
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
        print(unciphered_blocks[0])
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

#Función para exportar el archivo original: 
def write_unciphered_blocks(unciphered_data, filename=None):
    file_type = detect_file_type(unciphered_data)
    print(f"Tipo de archivo detectado: {file_type}")

    extension_map = {
        'PNG image': 'output.png',
        'JPEG image': 'output.jpg',
        'PDF document': 'output.pdf',
        'ZIP archive': 'output.zip',
        'MP3 audio': 'output.mp3',
        'Windows EXE': 'output.exe',
        'Plain text': 'output.txt',
        'Unknown file type': 'output.unknown'
    }
    filename = extension_map.get(file_type, 'output.unknown')
    with open(filename, "wb") as f:
        f.write(unciphered_data)
    print(f"Archivo descifrado guardado como: {filename}")

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

#Función para descifrar un bloque
def decipher_block(input_bytes, expanded_key):
    state = input_bytes
    state = add_round_key(state, expanded_key[40:44])
    for i in range(9, 0, -1):
        state = inv_shiftrows(state.reshape(4,4))
        state = inv_subbytes(state.flatten())
        state = add_round_key(state, expanded_key[i*4:(i+1)*4])
        state = state.reshape(4, 4)
        state = inverse_mixcolumns(state.T.flatten())
        state = state.reshape(4, 4).T
    state = inv_shiftrows(state)
    state = inv_subbytes(state.flatten())
    state = add_round_key(state, expanded_key[0:4])

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

#Función para descifrar un bloque en modo CBC
def decipher(input_bytes, expanded_key):
    unciphered_blocks = []
    i_vec = np.zeros(16, dtype = np.uint8)
    previous_block = i_vec

    for block in input_bytes:
        decrypted = decipher_block(block, expanded_key)
        plain_block = matrix_xor(decrypted, previous_block)
        unciphered_blocks.append(plain_block)
        previous_block = block
    return b"".join(block.tobytes() for block in unciphered_blocks)
        
#Funcion para identificar el tipo de archivo: 
def detect_file_type(decrypted_bytes):
    magic_numbers = {
        b'\x89PNG': 'PNG image',
        b'\xFF\xD8\xFF': 'JPEG image',
        b'%PDF': 'PDF document',
        b'PK\x03\x04': 'ZIP archive',
        b'ID3': 'MP3 audio',
        b'MZ': 'Windows EXE',
    }

    for magic, ftype in magic_numbers.items():
        if decrypted_bytes.startswith(magic):
            return ftype
    return "Unknown file type"

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
                    filename = input('\nDame el nombre del archivo a descifrar: ') #filename en string
                    key = ask_for_key() #lista de ints
                    expanded_key = key_expansion(key) #matriz de keys (c/elemento es una columna de 4 bytes)
                    result = decipher(read_file(filename), expanded_key)
                    write_unciphered_blocks(result)
                    break
                case _:
                    print("Opción no válida.")
        except ValueError:
            print("Por favor ingresa un número válido (1 o 2).")
                
main()