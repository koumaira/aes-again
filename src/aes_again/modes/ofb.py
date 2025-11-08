from ..aes_block import AESBlock
from ..utils import zero_iv
def encrypt(key,pt):
    a=AESBlock(key);iv=zero_iv();out=bytearray();state=iv
    for i in range(0,len(pt),16):
        state=a.encrypt_block(state)
        blk=pt[i:i+16]
        out+=bytes(x^y for x,y in zip(blk,state[:len(blk)]))
    return bytes(out)
def decrypt(key,ct):
    return encrypt(key,ct)
