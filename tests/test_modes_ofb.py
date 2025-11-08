from binascii import unhexlify
from aes_again.modes import ofb
from aes_again.utils import parse_key
def test_ofb_roundtrip():
    key=parse_key('2b7e151628aed2a6abf7158809cf4f3c')
    pt=unhexlify('6bc1bee22e409f96e93d7e11')
    ct=ofb.encrypt(key,pt)
    out=ofb.decrypt(key,ct)
    assert out==pt
