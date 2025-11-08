from ..aes_block import AESBlock
from ..padding import pad_zero_count,unpad_zero_count
def encrypt(key,pt):
    a=AESBlock(key)
    pt=pad_zero_count(pt,16)
    out=bytearray()
    for i in range(0,len(pt),16):
        out+=a.encrypt_block(pt[i:i+16])
    return bytes(out)
def decrypt(key,ct):
    a=AESBlock(key)
    out=bytearray()
    for i in range(0,len(ct),16):
        out+=a.decrypt_block(ct[i:i+16])
    return unpad_zero_count(bytes(out),16)
