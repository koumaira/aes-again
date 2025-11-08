from ..aes_block import AESBlock
from ..utils import parse_ctr,inc_ctr
def encrypt(key,pt,counter_hex=None):
    if counter_hex is None:raise ValueError('ctr required')
    ctr=parse_ctr(counter_hex)
    a=AESBlock(key);out=bytearray()
    for i in range(0,len(pt),16):
        ks=a.encrypt_block(bytes(ctr))
        blk=pt[i:i+16]
        out+=bytes(x^y for x,y in zip(blk,ks[:len(blk)]))
        inc_ctr(ctr)
    return bytes(out)
def decrypt(key,ct,counter_hex=None):
    return encrypt(key,ct,counter_hex)
