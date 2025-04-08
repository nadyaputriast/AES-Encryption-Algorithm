from KeyExpansion import key_expansion
from AddRoundKey import add_round_key
from SubBytes import sub_bytes
from ShiftRows import shift_rows
from MixColumns import mix_columns

def aes_encrypt(plaintext, key, debug=False):
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
    
    steps = []  # To store each step for debugging

    # Initial AddRoundKey
    state = add_round_key(state, round_keys[0])
    if debug:
        steps.append({"description": "Initial AddRoundKey", "state": convert_from_state_matrix(state)})

    # di rounds (Nr - 1)
    for round_num in range(1, Nr):
        state = sub_bytes(state)  # Substitution using S-Box
        if debug:
            steps.append({"description": f"Round {round_num} - SubBytes", "state": convert_from_state_matrix(state)})
        state = shift_rows(state)  # Shift rows
        if debug:
            steps.append({"description": f"Round {round_num} - ShiftRows", "state": convert_from_state_matrix(state)})
        state = mix_columns(state)  # Mix columns
        if debug:
            steps.append({"description": f"Round {round_num} - MixColumns", "state": convert_from_state_matrix(state)})
        state = add_round_key(state, round_keys[round_num])  # Add round key
        if debug:
            steps.append({"description": f"Round {round_num} - AddRoundKey", "state": convert_from_state_matrix(state)})

    # final round
    state = sub_bytes(state)
    if debug:
        steps.append({"description": "Final Round - SubBytes", "state": convert_from_state_matrix(state)})
    state = shift_rows(state)
    if debug:
        steps.append({"description": "Final Round - ShiftRows", "state": convert_from_state_matrix(state)})
    state = add_round_key(state, round_keys[Nr])
    if debug:
        steps.append({"description": "Final Round - AddRoundKey", "state": convert_from_state_matrix(state)})
    
    # Step 6: Convert State Matrix to Ciphertext
    ciphertext = convert_from_state_matrix(state)
    
    return (ciphertext, steps) if debug else ciphertext

# converting plaintext to state matrix (by column)
def convert_to_state_matrix(data):
    state = [[0 for _ in range(4)] for _ in range(4)]
    
    for i in range(4):
        for j in range(4):
            state[j][i] = data[i * 4 + j]
    
    return state

# converting state matrix to ciphertext (by column)
def convert_from_state_matrix(state):
    data = bytearray(16)
    
    for i in range(4):
        for j in range(4):
            data[i * 4 + j] = state[j][i]
    
    return bytes(data)