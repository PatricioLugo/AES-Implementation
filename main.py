from add_round_key import add_round_key_func
from expand_key import expand_key_func
from sub_bytes import subbytes
from inverse_sub_bytes import inverse_subbytes
from shift_rows import shiftrows
from inverse_shift_rows import inv_shiftrows
from mix_columns import mix_columns
from inverse_mix_columns import inverse_mixcolumns

def cipher(input_bytes, expanded_key):
    state = input_bytes
    state = add_round_key_func(state, expanded_key[0:16])
    for i in range(1, 10):
        state = subbytes(state)
        state = shiftrows(state)
        state = mix_columns(state)
        state = add_round_key_func(state, expanded_key[i*16:(i*16+15)])
    
    state = subbytes(state)
    state = shiftrows(state)
    state = add_round_key_func(state, expanded_key[160:176])

    return state
    
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


def main():
    print('Bienvenido al programa de encriptación y decriptación usando AES\n')
    while True:
        print('1. Cifrado')
        print('2. Descifrado')
        selection = int(input('Selecciona la opción deseada: '))
        if selection == 1:
            filename = input('\nDame el nombre del archivo a cifrar: ')
            #Llamada a función para cifrar
        elif selection == 2:
            filename = input('\nDame el nombre del archivo a descifrar: ')
            #Llamada a función a descifrar

print(read_file("example.txt"))