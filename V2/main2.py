from add_round_key2 import add_round_key_func
from expand_key2 import key_expansion
from sub_bytes2 import subbytes
from inverse_sub_bytes2 import inverse_subbytes
from shift_rows2 import shiftrows
from inverse_shift_rows2 import inv_shiftrows
from mix_columns2 import mix_columns
from inverse_mix_columns2 import inverse_mixcolumns
import numpy as np


'''
Falta terminar de crear funciones en main.
'''
## Función para leer el archivo
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
#Función para pedir la Key

#Función para exportar un archivo .aes

#Función para cifrar un bloque

#Función para cifrar en modo CBC

#Función para descifrar un bloque

#Función para descifrar en modo CBC

#Función main
def main(): 
    while True: 
        selection = input('1 para cifrado, 2 para descifrado: ') #Input en integer
        match selection:
            case 1: 
                filename = input('\n Dame el nombre del archivo a cifrar: ') #filename en string
                key = ask_for_key() #Lista de ints
                expanded_key = key_expansion(key) #Matriz de Keys (c/elemento es int)
                result = cipher(read_file(filename), expanded_key) #Lista de bloques de bytes de 16 bits c/uno
                write_ciphered_blocks(result, 'output.aes')
                


main()