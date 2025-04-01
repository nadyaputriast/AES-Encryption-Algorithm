from KeyExpansion import key_expansion
from AddRoundKey import add_round_key
from SubBytes import sub_bytes 
from ShiftRows import shift_rows
from MixColumns import mix_columns


def aes_encrypt(plaintext, key):
    if len(plaintext) != 16:
        raise ValueError("Plaintext must be exactly 16 bytes (128 bits)")
    
    key_bytes = len(key)
    if key_bytes == 16:      # 128-bit 
        Nr = 10
    elif key_bytes == 24:    # 192-bit 
        Nr = 12
    elif key_bytes == 32:    # 256-bit 
        Nr = 14
    else:
        raise ValueError("Key size must be 16, 24, or 32 bytes")
    
    # Key Expansion - membuat round keys
    round_keys = key_expansion(key)
    
    # inisialisasi state matrix (4x4)
    state = convert_to_state_matrix(plaintext)
    
    # ambil round
    state = add_round_key(state, round_keys[0])
    
    # di rounds (Nr - 1)
    for round_num in range(1, Nr):
        state = sub_bytes(state)     # bisa subtitusi S-Box
        state = shift_rows(state)     
        state = mix_columns(state)   
        state = add_round_key(state, round_keys[round_num]) 
    
    # final round
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[Nr])
    
    # Step 6: Convert State Matrix to Ciphertext
    ciphertext = convert_from_state_matrix(state)
    
    return ciphertext


def convert_to_state_matrix(data):
    state = [[0 for _ in range(4)] for _ in range(4)]
    
    for i in range(4):
        for j in range(4):
            state[j][i] = data[i * 4 + j]
    
    return state


def convert_from_state_matrix(state):
    data = bytearray(16)
    
    for i in range(4):
        for j in range(4):
            data[i * 4 + j] = state[j][i]
    
    return bytes(data)