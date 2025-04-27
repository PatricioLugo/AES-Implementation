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
main()