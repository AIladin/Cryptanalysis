from ukrainian_letter_frequences import UKRAINIAN_LETTER_FREQUENCES
import re
import numpy as np

abc = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'


def get_seq(ct, key_len):
    dt = {i: [] for i in range(key_len)}
    for i, lt in enumerate(ct):
        dt[i % key_len] += lt
    return list(dt.values())


def get_ioc(ct):
    if len(ct) < 2:
        return 0
    n = len(ct)
    res = 0
    for letter, dist in UKRAINIAN_LETTER_FREQUENCES.items():
        count = ct.count(letter)
        res += count*(count - 1)

    return res/(n*(n-1))


def get_hist(ct):
    hist = [0]*len(abc)
    for letter, dist in UKRAINIAN_LETTER_FREQUENCES.items():
        hist[abc.find(letter)] = ct.count(letter)
    return hist


def read_file(path):
    with open(path, 'r') as f:
        return re.sub(f"[^{abc}]", "", f.read().lower())


def check_error(pt, ct):
    return 1-(np.char.array(list(pt)) == np.char.array(list(ct))).mean()
