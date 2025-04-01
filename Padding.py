from Encrypt import aes_encrypt 

def pad_data(data, block_size=16):
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length]) * padding_length
    return data + padding

def derive_key(key_material, desired_length):
    if len(key_material) >= desired_length:
        return key_material[:desired_length]  
    result = b''
    while len(result) < desired_length:
        result += key_material
    return result[:desired_length]

def aes_encrypt_with_padding(plaintext, key_material, key_size=16):

    if isinstance(key_material, str):
        key_material = key_material.encode('utf-8')
    
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    

    key = derive_key(key_material, key_size)
    

    padded_plaintext = pad_data(plaintext)
    
    ciphertext = b''
    for i in range(0, len(padded_plaintext), 16):
        block = padded_plaintext[i:i+16]
        encrypted_block = aes_encrypt(block, key)
        ciphertext += encrypted_block
    
    return ciphertext