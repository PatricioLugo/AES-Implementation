def main():
    current_state = [
        [0x32, 0x88, 0x31, 0xe0],
        [0x43, 0x5a, 0x31, 0x37],
        [0xf6, 0x30, 0x98, 0x07],
        [0xa8, 0x8d, 0xa2, 0x34]
    ]

    example_key = [
        ['0x2b', '0x28', '0xab', '0x09'],
        ['0x7e', '0xae', '0xf7', '0xcf'],
        ['0x15', '0xd2', '0x15', '0x4f'],
        ['0x16', '0xa6', '0x88', '0x3c']
    ]

    result = add_round_key_func(current_state, example_key, 0)

    for row in result:
        print([f"0x{byte:02x}" for byte in row])

def add_round_key_func(state, roundkey, type):
    match type:
        case 0:
            roundkey = [[int(byte, 16) for byte in row] for row in roundkey] 
        case 1:
            pass  

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