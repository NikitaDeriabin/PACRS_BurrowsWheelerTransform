from random import choice
import random
from string import ascii_letters

length = 256
ls_ascii = list(ascii_letters)
with open('test.txt', 'w') as file:
    for _ in range(length):
        file.write(choice(ls_ascii))
