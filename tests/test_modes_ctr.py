from binascii import unhexlify
from aes_again.modes import ctr
from aes_again.utils import parse_key
def test_ctr_roundtrip():
    key=parse_key('2b7e151628aed2a6abf7158809cf4f3c')
    pt=unhexlify('6bc1bee22e409f96e93d7e117393172a3ad77b')
    ct=ctr.encrypt(key,pt,'f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff')
    out=ctr.decrypt(key,ct,'f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff')
    assert out==pt
