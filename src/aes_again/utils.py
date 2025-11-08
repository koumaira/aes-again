import binascii,sys,os
def read_file(p):
    with open(p,'rb') as f:
        return f.read()
def write_file(p,b):
    with open(p,'wb') as f:
        f.write(b)
def hex_to_bytes(h):
    return binascii.unhexlify(h.strip())
def bytes_to_hex(b):
    return binascii.hexlify(b).decode()
def zero_iv():
    return b'\x00'*16
def parse_key(key_hex):
    k=hex_to_bytes(key_hex)
    if len(k) not in (16,24,32):
        raise ValueError('key length invalid')
    return k
def parse_ctr(ctr_hex):
    c=hex_to_bytes(ctr_hex)
    if len(c)!=16:
        raise ValueError('ctr must be 16 bytes')
    return bytearray(c)
def inc_ctr(c):
    for i in range(15,-1,-1):
        c[i]=(c[i]+1)&0xff
        if c[i]!=0:break
    return c
