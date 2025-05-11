'''
INPUT: 16 byte block as a list of decimal formatted integers.

OUTPUT: 16 byte block as a list of decimal formatted integers.
'''
import numpy as np

def main():
    block = np.array([
        0x32, 0x88, 0x31, 0xe0,
        0x43, 0x5a, 0x31, 0x37,
        0xf6, 0x30, 0x98, 0x07,
        0xa8, 0x8d, 0xa2, 0x34
    ], dtype=np.uint8)

    key = np.array([
        [0x2b, 0x7e, 0x15, 0x16],
        [0x28, 0xae, 0xd2, 0xa6],
        [0xab, 0xf7, 0x15, 0x88],
        [0x09, 0xcf, 0x44, 0x3c]
    ], dtype=np.uint8)

    new_state = add_round_key(block, key)
    print("New State:")
    print(new_state)

def rearrange_key(key):
    new_key = np.zeros(16, dtype=np.uint8)

    cont = 0

    for i in range(4):
        for j in range(4):
            new_key[cont] = key[j][i]
            cont += 1

    return new_key

def add_round_key(block, key):
    ### Hay que corregir error en que block viene row-wise y key viene column-wise
    new_key = rearrange_key(key)

    new_block = np.zeros(16, dtype=np.uint8)

    for i in range(16):
        key_byte = new_key[i]
        xor_byte = block[i] ^ key_byte
        #print(f'X0R of block:{hex(block[i])} with key:{hex(key_byte)} = {hex(xor_byte)}')
        new_block[i] = xor_byte
    
    return new_block

if __name__ == "__main__":
    main()