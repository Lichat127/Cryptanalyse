import math
import sys
import argparse
import os
import re

INIT = 0
ROUNDED = 3
UPPER_A_CODE = 65
UPPER_Z_CODE = 90
LOWER_A_CODE = 97
LOWER_Z_CODE = 122
ALPHABET_LENGTH = 26


key_letter_division = {}
decrypted_messages = []
frequency_analysis_decrypted_messages = []
key_dico = []



def main() :

    message = get_message()
    formated_message = format_message(message)

    find_keys(formated_message)

    for key in key_dico :
        vigenere(message, key)

    get_decrypted_text()
    get_result(message)





def get_message():

    parser = argparse.ArgumentParser(description = "Mon programme python")
    parser.add_argument("-f", "--file", help="Nom du fichier à traiter")
    args = parser.parse_args()

    if args.file :
        file_source = open(args.file, "r")
        message = file_source.read()
        file_source.close()
    else :
        message = input("Entrez le message à déchiffré : ")

    return(message)





def format_message(message) :

    formated_message = ""

    for letter in message :
        if ord(letter) >= LOWER_A_CODE and ord(letter) <= LOWER_Z_CODE :
            formated_message = formated_message + letter

        elif ord(letter) >= UPPER_A_CODE and ord(letter) <= UPPER_Z_CODE :
            formated_message = formated_message + letter.lower()

    return(formated_message)




def find_keys(formated_message):

    for len_key in range(2, 20):

        potential_key = ""

        for i in range (INIT, len_key):
            key_letter_division[i] = ""

        message_group = re.findall(f".{{1,{len_key}}}", formated_message)

        for group in message_group :
            index = 0
            for letter in group :
                key_letter_division[index] += str(letter)
                index += 1

        for i in key_letter_division :
            max_letter = frequency_analysis(key_letter_division.get(i), "alphabet")

            if key_letter_division.get(i) != "":
                decalage = ord(max_letter) - ord("e")
                key_letter = ((ord("a") - LOWER_A_CODE + decalage) % ALPHABET_LENGTH) + LOWER_A_CODE
                new_key_letter = chr(key_letter)
                potential_key = potential_key + new_key_letter
            else :
                break

        key_letter_division.clear()
        key_dico.append(potential_key)

    return(key_dico)





def frequency_analysis(message, dico) :

    len_message = INIT

    if dico == "alphabet" :
        alphabet = {"a":0, "b":0, "c":0, "d":0,"e":0,"f":0,"g":0,"h":0,"i":0,"j":0,"k":0,"l":0,"m":0,"n":0,"o":0,"p":0,"q":0,"r":0,"s":0,"t":0,"u":0,"v":0,"w":0,"x":0,"y":0,"z":0,"none" : 0}
        max_letter = "none"
    if dico == "bigrammes" :
        alphabet = {"dansle":0,"lement":0,"quelle":0,"quelqu":0,"uelque":0,"dansla":0,"endant":0,"taient":0,"encore":0,"ementd": 0, "none" : 0}
        max_letter = "none"

    for letter in alphabet :
        alphabet[letter] = message.count(letter)
        len_message = len_message + alphabet.get(letter)

    if len_message != 0:
        for letter in alphabet :
            alphabet[letter] = round(alphabet.get(letter) / len_message, ROUNDED)
            alphabet[letter] = alphabet.get(letter)


        for letter in alphabet :
            if alphabet.get(max_letter) < alphabet.get(letter) :
                max_letter = letter
    else :
        max_letter = "none"

    if dico == "alphabet" :
        return(max_letter)

    if dico == "bigrammes" :
        frequency_analysis_decrypted_messages.append(max_letter)

    alphabet.clear()





def vigenere(message, key) :

    alphabet_maj = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")

    alphabet_min = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

    decrypted_message = ""
    new_letter = ""
    key_list = list(key)
    index_key = INIT
    for letter in message :
        if index_key >= len(key_list) :
            index_key = INIT

        if ord(letter) >= LOWER_A_CODE and ord(letter) <= LOWER_Z_CODE :
            decalage = alphabet_min.index(key_list[index_key]) + 1
            new_letter = ((alphabet_min.index(letter) + 1 - decalage) % ALPHABET_LENGTH)
            new_letter = alphabet_min[new_letter]
            index_key = index_key + 1

        elif ord(letter) >= UPPER_A_CODE and ord(letter) <= UPPER_Z_CODE :
            decalage = alphabet_min.index(key_list[index_key]) + 1
            new_letter = ((alphabet_maj.index(letter) + 1 - decalage) % ALPHABET_LENGTH)
            new_letter = alphabet_maj[new_letter]
            index_key = index_key + 1

        else :
            new_letter = letter

        decrypted_message = decrypted_message + new_letter

    decrypted_messages.append(decrypted_message)




def get_decrypted_text() :

    for message in decrypted_messages :
        frequency_analysis(message, "bigrammes")

    hexagrammes = ("dansle", "lement", "quelle","quelqu","uelque","dansla","endant","taient","encore","ementd")
    for i in range(0,18) :
        for hexagramme in hexagrammes :
            if frequency_analysis_decrypted_messages[i] == hexagramme :
                    print(f"MESSAGE DECHIFFRE : \n{decrypted_messages[i]}")
                    print(f"CLE : {key_dico[i]}")
                    continue
    print(frequency_analysis_decrypted_messages)





def get_result(message) :

    if os.path.exists("resultVigenere.txt") :
        os.remove("resultVigenere.txt")

    file_destination = open("resultVigenere.txt", "a")

    file_destination.write(f" - MESSAGE CHIFFRE - \n{message}")

    file_destination.write("\n - POTENTIELLES CLES - \n")
    for key in key_dico :
        file_destination.write(f"{key}\n")

    file_destination.write(f"\n -  -")
    file_destination.close()

if __name__ == "__main__" :
    main()
