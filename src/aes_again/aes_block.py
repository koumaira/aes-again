from Crypto.Cipher import AES
class AESBlock:
    def __init__(self,key:bytes):
        self.key=key
    def encrypt_block(self,block16:bytes)->bytes:
        return AES.new(self.key,AES.MODE_ECB).encrypt(block16)
    def decrypt_block(self,block16:bytes)->bytes:
        return AES.new(self.key,AES.MODE_ECB).decrypt(block16)
