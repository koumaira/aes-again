import sys,os
import streamlit as st
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
SRC=os.path.join(ROOT,'src')
if SRC not in sys.path:sys.path.insert(0,SRC)
from aes_again.utils import parse_key,hex_to_bytes,bytes_to_hex
from aes_again.modes import ecb,cbc,cfb,ofb,ctr
import string as _s
import re as _re

def looks_printable(b:bytes):
    t=b.decode('utf-8','ignore')
    if not t:return ''
    ok=sum(ch in _s.printable for ch in t)
    return t if ok/max(1,len(t))>0.8 else ''

def is_hex_like(s:str)->bool:
    s=s.strip()
    return len(s)%2==0 and bool(_re.fullmatch(r'[0-9a-fA-F]+',s))

st.set_page_config(page_title='AES Again',page_icon='🔐',layout='centered')
st.title('AES Again 🔐')
st.caption('ECB • CBC • CFB • OFB • CTR')

with st.sidebar:
    mode=st.selectbox('Mode',['cbc','ecb','cfb','ofb','ctr'],index=0)
    op=st.selectbox('Operation',['enc','dec'],index=0)
    key_hex=st.text_input('Key (hex)','2b7e151628aed2a6abf7158809cf4f3c')
    ctr_hex=st.text_input('Counter (hex, CTR only)','f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff') if mode=='ctr' else None
    auto=st.checkbox('Auto-detect hex',value=True)
    hex_io=st.checkbox('Hex input/output',value=False)
    run=st.button('Run')

tabs=st.tabs(['Text','File'])

def run_bytes(data:bytes)->bytes:
    k=parse_key(key_hex)
    if mode=='ecb':
        return ecb.encrypt(k,data) if op=='enc' else ecb.decrypt(k,data)
    if mode=='cbc':
        return cbc.encrypt(k,data) if op=='enc' else cbc.decrypt(k,data)
    if mode=='cfb':
        return cfb.encrypt(k,data) if op=='enc' else cfb.decrypt(k,data)
    if mode=='ofb':
        return ofb.encrypt(k,data) if op=='enc' else ofb.decrypt(k,data)
    return ctr.encrypt(k,data,ctr_hex) if op=='enc' else ctr.decrypt(k,data,ctr_hex)

with tabs[0]:
    txt=st.text_area('Input','hello aes again',height=140)
    if run:
        try:
            use_hex=hex_io or (auto and is_hex_like(txt))
            data=hex_to_bytes(txt.strip()) if use_hex else txt.encode()
            out=run_bytes(data)
            if use_hex:
                st.code(bytes_to_hex(out))
                prev=looks_printable(out)
                if prev:
                    st.text_area('Plaintext preview',prev,height=120)
            else:
                st.code(out.hex(),language='text')
                st.download_button('Download result',out,file_name='result.bin')
        except Exception as e:
            st.error(str(e))

with tabs[1]:
    up=st.file_uploader('Upload file',type=None)
    if run and up is not None:
        try:
            data=up.read()
            out=run_bytes(data)
            st.success('Done')
            st.download_button('Download result',out,file_name=(up.name+'.out'))
        except Exception as e:
            st.error(str(e))
