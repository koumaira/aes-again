from binascii import unhexlify
from aes_again.modes import ecb
from aes_again.utils import parse_key
def test_ecb_roundtrip():
    key=parse_key('2b7e151628aed2a6abf7158809cf4f3c')
    pt=unhexlify('6bc1bee22e409f96e93d7e117393172a000102030405060708090a0b0c0d0e0f')
    ct=ecb.encrypt(key,pt)
    out=ecb.decrypt(key,ct)
    assert out==pt
