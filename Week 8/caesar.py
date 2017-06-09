import cs50
import sys

def main():
    if len(sys.argv) != 2:
        print("Give command line arguments!")
        exit(1)
    
    key = int(sys.argv[1])
    arr = []
    message = cs50.get_string()
    for symbol in message:
        if symbol.isalpha():
            arr.append(caesar(symbol, key))
        else:
            arr.append(symbol)
                
    print("".join(arr))
    exit(0)

def caesar(char, key):
    if char.isupper():
        return chr(((ord(char) - 65 + key) % 26) + 65)
    else:
        return chr(((ord(char) - 97 + key) % 26) + 97)
        
if __name__ == "__main__":
    main()