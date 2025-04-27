def main():
    current_state = [
        [0x32, 0x88, 0x31, 0xe0],
        [0x43, 0x5a, 0x31, 0x37],
        [0xf6, 0x30, 0x98, 0x07],
        [0xa8, 0x8d, 0xa2, 0x34]
    ]

    example_key = [
        ['2b', '28', 'ab', '09'],
        ['7e', 'ae', 'f7', 'cf'],
        ['15', 'd2', '15', '4f'],
        ['16', 'a6', '88', '3c']
    ]
    
    int_key = [[int(byte, 16) for byte in row] for row in example_key]

    result = add_round_key_func(current_state, int_key)

    for row in result:
        print([f"0x{byte:02x}" for byte in row])

def add_round_key_func(state, roundkey):
    result = []

    for row in range(4):
        new_row = []

        for col in range(4):
            xor_byte = state[row][col] ^ roundkey[row][col]
            new_row.append(xor_byte)

        result.append(new_row)

    for i, row in enumerate(result):
        for j, element in enumerate(row):
            result[i][j] = int(element)

    return result

if __name__ == "__main__":
    main()