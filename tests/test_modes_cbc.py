from binascii import unhexlify
from aes_again.modes import cbc
from aes_again.utils import parse_key
def test_cbc_roundtrip():
    key=parse_key('603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4')
    pt=unhexlify('6bc1bee22e409f96e93d7e117393172a3ad77bb40d7a3660a89ecaf32466ef97')
    ct=cbc.encrypt(key,pt)
    out=cbc.decrypt(key,ct)
    assert out==pt
