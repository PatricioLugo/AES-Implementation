def main():

    example_state = [['0x19', '0xa0', '0x9a', '0xe9'],
                    ['0x3d', '0xf4', '0xc6', '0xf8'],
                    ['0xe3', '0xe2', '0x8d', '0x48'],
                    ['0xbe', '0x2b', '0x2a', '0x08']]
    
    shifted_state =shiftrows(example_state)
    print(shifted_state)

def shiftrows(state):
    state = [[int(byte, 16) for byte in row] for row in state]

    #Start state 
    # [[0x19, 0xa0, 0x9a, 0xe9],
      #[0x3d, 0xf4, 0xc6, 0xf8],
      #[0xe3, 0xe2, 0x8d, 0x48],
      #[0xbe, 0x2b, 0x2a, 0x08]]

    #End state 
    # [[0x19, 0xa0, 0x9a, 0xe9],    Remains unshifted 
      #[0xf4, 0xc6, 0xf8, 0x3d],    Shift 1 to the left
      #[0x8d, 0x48, 0xe3, 0xe2],    Shift 2 to the left
      #[0x08, 0xbe, 0x2b, 0x21]]    Shift 3 to the left

#Second row 
    state[1] = state[1][1:]+ state[1][:1]
#Third row
    state[2] = state[2][2:] + state[2][:2]
#Fourth row
    state[3] = state[3][3:] + state[3][:3]

    return state

if __name__ == "__main__":
    main()

