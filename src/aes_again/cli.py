import argparse,sys
from .utils import read_file,write_file,bytes_to_hex,hex_to_bytes,parse_key
from .modes import ecb,cbc,cfb,ofb,ctr
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mode',required=True,choices=['ecb','cbc','cfb','ofb','ctr'])
    p.add_argument('--op',required=True,choices=['enc','dec'])
    p.add_argument('--key',required=True)
    p.add_argument('--ctr')
    p.add_argument('--in')
    p.add_argument('--out')
    p.add_argument('--hex-in',action='store_true')
    p.add_argument('--hex-out',action='store_true')
    a=p.parse_args()
    key=parse_key(a.key)
    data=read_file(a.__dict__['in']) if a.__dict__['in'] else sys.stdin.buffer.read()
    if a.hex_in:data=hex_to_bytes(data.decode().strip())
    if a.mode=='ecb':
        res=ecb.encrypt(key,data) if a.op=='enc' else ecb.decrypt(key,data)
    elif a.mode=='cbc':
        res=cbc.encrypt(key,data) if a.op=='enc' else cbc.decrypt(key,data)
    elif a.mode=='cfb':
        res=cfb.encrypt(key,data) if a.op=='enc' else cfb.decrypt(key,data)
    elif a.mode=='ofb':
        res=ofb.encrypt(key,data) if a.op=='enc' else ofb.decrypt(key,data)
    else:
        if not a.ctr:raise SystemExit('ctr required for ctr mode')
        res=ctr.encrypt(key,data,a.ctr) if a.op=='enc' else ctr.decrypt(key,data,a.ctr)
    out=(bytes_to_hex(res)+'\n').encode() if a.hex_out else res
    (open(a.out,'wb').write(out) if a.out else sys.stdout.buffer.write(out))
if __name__=='__main__':
    main()
