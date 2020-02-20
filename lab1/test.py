import numpy as np
from itertools import permutations, product
import progressbar
from math import factorial


def make_box(line):
    return np.array(list(line)).reshape(2, 2)

def make_key(line1, line2, line3, line4):
    return np.array([make_box(line1),
                     make_box(line2),
                     make_box(line3),
                     make_box(line4)])

abc = 'abcd'


def enc_bigram(key, bigram):
    y1, x1 = np.where(key[0]==bigram[0])
    y1, x1 = y1[0], x1[0]

    y2, x2 = np.where(key[3]==bigram[1])
    y2, x2 = y2[0], x2[0]

    return key[1][y1][x2], key[2][y2][x1]


def dec_bigram(key, bigram):
    y1, x1 = np.where(key[1]==bigram[0])
    y1, x1 = y1[0], x1[0]

    y2, x2 = np.where(key[2]==bigram[1])
    y2, x2 = y2[0], x2[0]

    return key[0][y1][x2], key[3][y2][x1]



def check_key(key):
    valid = True
    bigrams = {}
    for bigram in product(abc, repeat=2):
        bigrams[bigram] = {enc_bigram(key, bigram)}

        if bigram == enc_bigram(key, bigram):
            valid=False
            print(bigram, bigrams[bigram])

    if valid: print(*[f'{k}->{v}' for k, v in bigrams.items()], sep='\n')
    return valid
p1 = 'pgdbaqnhecuroifxvsmkzywtl'
p2 = 'zxutlyvrmgwsnhdqoiebpkfca'
p3 = 'lquxzgmrvydhnswbeiotacfkp'
p4 = 'yuiopcvbnmqwertasdfghklzx'

#key1 = make_key(abc, abc, abc, abc)
#key2 = make_key(abc, abc, abc, p4)

# print(check_key(key2))
# wc = make_key(abc, abc, abc, make_box('aabc'))
# wbigams = {}
# for bi  in permutations(abc, 2):
#     wbigrams[bi] = enc_bigram(wc, bi)
#
# for p1 :
#     bigrams = {}
#     wbigams = {}
#     np.random.shuffle(key1[0])
#     np.random.shuffle(key1[1])
#     np.random.shuffle(key1[2])
#     np.random.shuffle(key1[3])
#     np.random.shuffle(key2[0])
#     np.random.shuffle(key2[1])
#     np.random.shuffle(key2[2])
#     np.random.shuffle(key2[3])
#     for bi  in permutations(abc, 2):
#         bigrams[bi] = enc_bigram(key2, enc_bigram(key1, bi))
#         print(bigrams.values())
#     if len(set(bigrams.keys()))!=12:
#         print(key1, key2)
#         break
#

bigrams = set()
for p1 in permutations(abc):
    for p2 in permutations(abc):
        for p3 in permutations(abc):
            for p4 in permutations(abc):
                for q1 in permutations(abc):
                    for q2 in permutations(abc):
                        for q3 in permutations(abc):
                            for q4 in permutations(abc):

                                key = make_key(p1, p2, p3, p4)
                                key1 = make_key(p1, p2, p3, p4)
                                print(key, key1)
                                for bi in product(abc, repeat=2):
                                    bigrams.add(enc_bigram(key1,
                                     enc_bigram(key, 2)))
print(sorted(bigrams))
