import os
from aes_again.padding import pad_zero_count,unpad_zero_count
def test_roundtrip():
    for n in range(0,64):
        b=os.urandom(n)
        x=pad_zero_count(b,16)
        y=unpad_zero_count(x,16)
        assert y==b
def test_exact_multiple():
    b=b'a'*16
    x=pad_zero_count(b,16)
    assert len(x)%16==0
    y=unpad_zero_count(x,16)
    assert y==b
