import math
import sys
import argparse
import os

INIT = 0
ROUNDED = 3
UPPER_A_CODE = 65
UPPER_Z_CODE = 90
LOWER_A_CODE = 97
LOWER_Z_CODE = 122
ALPHABET_LENGTH = 26

alphabet = {"a" : 0, "b" : 0, "c" : 0, "d" : 0, "e" : 0, "f" : 0, "g" : 0, "h" : 0, "i" : 0, "j" : 0, "k" : 0, "l" : 0, "m" : 0, "n" : 0, "o" : 0, "p" : 0, "q" : 0, "r" : 0, "s" : 0, "t" : 0, "u" : 0, "v" : 0, "w" : 0, "x" : 0, "y" : 0, "z" : 0}


def main() :

    message = get_message()
    message_list = list(message.lower())

    result = frequency_analysis(message_list)

    new_message = Caesar(message, result[0])

    print(f"MESSAGE DECHIFFRE : \n{new_message}")

    put_info_in_fileresult(message, result[1], result[0], new_message)


def get_message() :

    parser = argparse.ArgumentParser(description = "Mon programme Python")
    parser.add_argument("-f", "--file", help="Nom du fichier à traiter")

    args = parser.parse_args()

    if args.file :
        file_source = open(args.file,"r")
        message = file_source.read()
        file_source.close()
    else :
        message = input("Entrez votre message :")

    return(message)





def frequency_analysis(message_list) :

    max_letter = "a"

    index_of_coincidence = INIT
    len_message = INIT

    for key in alphabet :
        alphabet[key] = message_list.count(key)
        len_message = len_message + alphabet.get(key)

    for key in alphabet :
        alphabet[key]= round(alphabet.get(key) / len_message,ROUNDED)
        alphabet[key]= alphabet.get(key)
        if alphabet.get(max_letter) < alphabet.get(key) :
            max_letter = key
        index_of_coincidence = index_of_coincidence + (alphabet.get(key) * alphabet.get(key))

    decalage = ord(max_letter) - ord("e")
    print(f"Le décalage est de : {decalage}")

    return(decalage, index_of_coincidence)





def Caesar(message, decalage):
    message_list = list(message)
    new_message = ""
    new_letter = ""

    for letter in message_list :
        if ord(letter) >= LOWER_A_CODE and ord(letter) <= LOWER_Z_CODE :
            new_letter = ((ord(letter) - LOWER_A_CODE - decalage) %
                    ALPHABET_LENGTH) + LOWER_A_CODE
            new_letter = chr(new_letter)
            new_message = new_message + new_letter
        elif ord(letter) >= UPPER_A_CODE and ord(letter) <= UPPER_Z_CODE :
            new_letter = ((ord(letter) - UPPER_A_CODE - decalage) % ALPHABET_LENGTH) + UPPER_A_CODE
            new_letter = chr(new_letter)
            new_message = new_message + new_letter
        else :
            new_message = new_message + letter

    return(new_message)





def put_info_in_fileresult(message, index_of_coincidence, decalage, new_message) :

    if os.path.exists("result.txt") :
        os.remove("result.txt")

    file_destination = open("result.txt", "a")

    file_destination.write(f" - MESSAGE CHIFFRE - \n{message}\n\n -ANALYSE FREQUENTIELLE-\n")
    for letter in alphabet :
        file_destination.write(f"{letter}  |  {alphabet.get(letter)}\n")
    file_destination.write(f"\nIndice de coincidence = {index_of_coincidence}\n")
    file_destination.write(f"\nDecalage = {decalage}\n")
    file_destination.write(f"\n - MESSAGE DECHIFFRE - \n{new_message}")
    file_destination.close()


if __name__ == "__main__" :
    main()


## A FAIRE
# - "-h" et autres arguments
