from utils import abc


def encrypt(key, pt):
    ct = ''
    for t, k in zip(pt, key*(1 + len(pt)//len(key))):
        ct += abc[(abc.find(t) + abc.find(k)) % len(abc)]
    return ct


def decrypt(key, ct):
    pt = ''
    for t, k in zip(ct, key*(1 + len(ct)//len(key))):
        pt += abc[(abc.find(t) - abc.find(k)) % len(abc)]
    return pt
