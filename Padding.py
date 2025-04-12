from Encrypt import aes_encrypt

# adding padding to plaintext to make it a multiple of 16 bytes
def pad_data(data, block_size=16):
    if isinstance(data, str):
        data = data.encode('utf-8')

    remainder = len(data) % block_size
    if remainder == 0:
        # Jika data sudah merupakan kelipatan block_size, tambahkan blok penuh padding
        padding_length = block_size
    else:
        padding_length = block_size - remainder
    
    padding = bytes([padding_length]) * padding_length
    return data + padding

# to ensure the key is having the desired length (16/24/32 bytes)
def derive_key(key_material, desired_length):
    if isinstance(key_material, str):
        key_material = key_material.encode('utf-8')
        
    if len(key_material) >= desired_length:
        return key_material[:desired_length]  
    
    result = b''
    while len(result) < desired_length:
        result += key_material
    return result[:desired_length]

# encrypt each block of plaintext using AES with padding
def aes_encrypt_with_padding(plaintext, key_material, key_size, debug=False):
    if isinstance(key_material, str):
        key_material = key_material.encode('utf-8')
    
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    key = derive_key(key_material, key_size)
    padded_plaintext = pad_data(plaintext, 16)
    
    ciphertext = b''
    steps = []  # To store all steps if debugging is enabled
    
    for i in range(0, len(padded_plaintext), 16):
        block = padded_plaintext[i:i+16]
        if debug:
            encrypted_block, block_steps = aes_encrypt(block, key, debug=True)
            for step in block_steps:
                step["block"] = i // 16
            steps.extend(block_steps)
        else:
            encrypted_block = aes_encrypt(block, key)
        ciphertext += encrypted_block

    return (ciphertext, steps) if debug else ciphertext

# encrypt each block of plaintext using AES without padding
def aes_encrypt_without_padding(plaintext, key_material, key_size, debug=False):
    if isinstance(key_material, str):
        key_material = key_material.encode('utf-8')
    
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    # Verify the plaintext length is a multiple of 16 bytes
    if len(plaintext) % 16 != 0:
        raise ValueError("Plaintext length must be a multiple of 16 bytes when not using padding")

    key = derive_key(key_material, key_size)
    
    ciphertext = b''
    steps = []  # To store all steps if debugging is enabled
    
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        if debug:
            encrypted_block, block_steps = aes_encrypt(block, key, debug=True)
            for step in block_steps:
                step["block"] = i // 16
            steps.extend(block_steps)
        else:
            encrypted_block = aes_encrypt(block, key)
        ciphertext += encrypted_block

    return (ciphertext, steps) if debug else ciphertext