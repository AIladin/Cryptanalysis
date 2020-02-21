from vigenere_cipher import decrypt
from utils import *
import numpy as np
from scipy.stats import chisquare

v_ioc = np.vectorize(get_ioc)

global_ioc = get_ioc(read_file('катерина.txt'))


def get_key_len(ct, max_len=33):
    res = []
    for i in range(2, max_len+1):
        seq = np.array(get_seq(ct, i))
        ioc = v_ioc(seq)
        res.append(ioc.mean())
    #print(*zip(np.argsort(res), res), sep="\n")
    return np.argmin(np.abs(np.array(res) - global_ioc)) + 2


def get_key(ct, key_len):

    key = ['_']*key_len
    split_text = np.array(get_seq(ct, key_len))
    for i, seq in enumerate(split_text):
        st = float('inf')
        for letter in abc:
            ch2 = chisquare(get_hist(decrypt(letter, seq)),
            list(UKRAINIAN_LETTER_FREQUENCES.values()))[0]
            if ch2 < st:
                st = ch2
                key[i] = letter

    return ''.join(key)



def analyze_encrypted_text(text):
    print(f"Used IOC {global_ioc}")
    proposed = ""
    key_len = get_key_len(text)
    print(f"[1/3] ### Key length: {key_len}")
    key = get_key(text, key_len)
    print(f"[2/3] ### Key: {key}")
    proposed = decrypt(key, text)
    print(f"[3/3] ### Finished!")
    return proposed
