from ..aes_block import AESBlock
from ..padding import pad_zero_count,unpad_zero_count
from ..utils import zero_iv
def xor(a,b):return bytes(x^y for x,y in zip(a,b))
def encrypt(key,pt):
    a=AESBlock(key);iv=zero_iv()
    pt=pad_zero_count(pt,16);c=bytearray();prev=iv
    for i in range(0,len(pt),16):
        blk=pt[i:i+16]
        prev=a.encrypt_block(xor(blk,prev))
        c+=prev
    return bytes(c)
def decrypt(key,ct):
    a=AESBlock(key);iv=zero_iv();out=bytearray();prev=iv
    for i in range(0,len(ct),16):
        cur=ct[i:i+16]
        out+=xor(a.decrypt_block(cur),prev)
        prev=cur
    return unpad_zero_count(bytes(out),16)
