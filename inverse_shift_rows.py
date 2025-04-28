def main(): 
    example_state = [[0x19, 0xa0, 0x9a, 0xe9], 
                 [0xf4, 0xc6, 0xf8, 0x3d], 
                 [0x8d, 0x48, 0xe3, 0xe2], 
                 [0x8, 0xbe, 0x2b, 0x2a]]
    
    shifted_inv_state = inv_shiftrows(example_state)
    print(shifted_inv_state)

def inv_shiftrows(state):  
    state = [[int(byte, 16) for byte in row] for row in state]  
    # Start state 
    # [[0x19, 0xa0, 0x9a, 0xe9],   
    #  [0xf4, 0xc6, 0xf8, 0x3d],    
    #  [0x8d, 0x48, 0xe3, 0xe2],    
    #  [0x8, 0xbe, 0x2b, 0x2a]]    

    # End state
    # [[0x19, 0xa0, 0x9a, 0xe9],   Remains unshifted 
    #  [0x3d, 0xf4, 0xc6, 0xf8],    Shift 1 to the right
    #  [0xe3, 0xe2, 0x8d, 0x48],    Shift 2 to the right
    #  [0xbe, 0x2b, 0x2a, 0x08]]    Shift 3 to the right

    # Second row
    state[1] = state[1][-1:] + state[1][:-1]

    # Third row 
    state[2] = state[2][-2:] + state[2][:-2]

    # Fourth row 
    state[3] = state[3][-3:] + state[3][:-3]

    return state

if __name__ == "__main__": 
    main()
    
