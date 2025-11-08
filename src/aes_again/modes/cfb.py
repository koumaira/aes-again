from ..aes_block import AESBlock
from ..utils import zero_iv
def encrypt(key,pt):
    a=AESBlock(key);iv=zero_iv();out=bytearray();state=iv
    for i in range(0,len(pt),16):
        ks=a.encrypt_block(state)
        blk=pt[i:i+16]
        ct=bytes(x^y for x,y in zip(blk,ks[:len(blk)]))
        out+=ct
        if len(blk)==16:state=ct
        else:state=(state[len(blk):]+ct)
    return bytes(out)
def decrypt(key,ct):
    a=AESBlock(key);iv=zero_iv();out=bytearray();state=iv
    for i in range(0,len(ct),16):
        ks=a.encrypt_block(state)
        blk=ct[i:i+16]
        pt=bytes(x^y for x,y in zip(blk,ks[:len(blk)]))
        out+=pt
        if len(blk)==16:state=blk
        else:state=(state[len(blk):]+blk)
    return bytes(out)
