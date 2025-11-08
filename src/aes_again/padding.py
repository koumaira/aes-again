def pad_zero_count(b,block_size=16):
    r=len(b)%block_size
    p=block_size if r==0 else block_size-r
    if p<1 or p>block_size:raise ValueError('pad')
    return b+b'\x00'*(p-1)+bytes([p])
def unpad_zero_count(b,block_size=16):
    if len(b)==0 or len(b)%block_size!=0:raise ValueError('bad length')
    p=b[-1]
    if p<1 or p>block_size:raise ValueError('bad pad')
    if b[-p:-1]!=b'\x00'*(p-1):raise ValueError('bad pad')
    return b[:-p]
