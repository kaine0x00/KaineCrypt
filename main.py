import argparse

def str_to_bin(st: str):
    return ''.join(format(ord(char), '08b') for char in st)


def bin_to_str(bin: str):
    return ''.join(chr(int(bin[i:i+8], 2)) for i in range(0, len(bin), 8))


def KaineCrypt(data: str, key: str):
    hash = ""
    key = key + "7842"  # Step 1: mutate key
    # Step 2: turn data and key to binary, we are going to do binary manip
    bData = str(str_to_bin(data)).replace(" ", "")
    bKey = str(str_to_bin(key)).replace(" ", "")
    # Step 3: Binary XOR
    hash = "".join("1" if a != b else "0" for a, b in zip(bKey,bData))
    # Step 4: convert hash to text
    hash = bin_to_str(hash)
    # Step 5: use dictionary and key to add seemingly random chars
    digit_symbols = {
        '0': '@',
        '1': '#',
        '2': 'C',
        '3': 'D',
        '4': '$',
        '5': 'F',
        '6': 'G',
        '7': '&',
        '8': 'I',
        '9': 'J'
    }

    for i in str(key):
        hash += digit_symbols[i]

    # Step 6: add some watermark salt
    hash = ''.join(["$k$", hash])
    return hash


def deKaineCrypt(hash: str, key: str):
    key = key + "7842"  # Key mutation
    plain_text = hash.replace("$k$", "", 1)    # Watermark removal
    digit_symbols = {
        '0': '@',
        '1': '#',
        '2': 'C',
        '3': 'D',
        '4': '$',
        '5': 'F',
        '6': 'G',
        '7': '&',
        '8': 'I',
        '9': 'J'
    }

    symbols_to_remove = ""

    for i in str(key):
        symbols_to_remove += digit_symbols[i]
    
    cut = len(symbols_to_remove)
    plain_text = plain_text[:-cut]
    # format everything to binary to undo the binary manipulation
    plain_text = str(str_to_bin(plain_text)).replace(" ", "")
    bKey = str(str_to_bin(key)).replace(" ", "")
    # undo the XOR with another XOR
    plain_text = "".join("1" if a != b else "0" for a, b in zip(bKey,plain_text))
    # back to text
    plain_text = bin_to_str(plain_text)
    return plain_text

def main():
    print("""BEWARE!!! THIS ISN'T A SAFE ENCRYPTION ALGORITHM AND IS INTENDED FOR PURELY EDUCATIONAL PURPOSES
          Because of the limitations of binary operations in python, the charset for passwords is quite limited, works best with:
          a - z
          a few special characters are okay: @ ^ 
          """)
    parser = argparse.ArgumentParser(description='KaineCrypt Terminal App')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Ecrypt data using KaineCrypt')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt a KaineCrypt hash')
    
    args = parser.parse_args()
    
    data = input("Input the text or hash: ")
    
    print("\n")
    key = input("Input the key/seed to use: ")
    # The key must be long to prevent it being shorter than the text binary
    if len(key) < 40:
        key = input("Sorry, the key isn't long enough, try again: ")

    if args.encrypt:
        for i in [data]: 
            if i not in "abcdefghijklmnopqrstuvwxyz@^":
                data = input("Sorry, the password is out of the charset, try again: ")
        encrypted = KaineCrypt(data, key)
        print("Your hash is: ", encrypted)
    elif args.decrypt:
        decrypted = deKaineCrypt(data, key)
        print("Your hash has been decrypted, the password was: ", decrypted)
    else:
        print("""Incorrect use of attributes, try with theese options:
              KaineCrypt/main.py [-e / -d]

              -e or --encrypt to specify you are going to encrypt data
              -d or --decrypt to specify you are going to decrypt a KaineCrypt hash
              """)
        
if __name__ == "__main__":
    main()