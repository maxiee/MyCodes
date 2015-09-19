__author__ = 'maxiee'
import string
import random


def gen_string_list(length):
    l = []
    for i in range(length):
        l.append(random.choice(string.ascii_letters))
    return l