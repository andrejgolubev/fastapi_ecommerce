from random import randint
from string import ascii_letters, digits

logic={
    1: ascii_letters, 
    2: digits
}

def beliberda(length=16): 
    string=''
    for i in range(length): 
        choice = logic[randint(1,2)]
        next_char = choice[randint(0,len(choice)-1)]

        string += next_char
    return string 

