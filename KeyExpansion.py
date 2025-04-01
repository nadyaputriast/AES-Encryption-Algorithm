from tabel import tabel

def key_expansion(key):
    s_box, Rcon = tabel()
    # konstantanya nanti berdasarkan dari panjang key yang digunakan
    key_bytes = len(key)
    if key_bytes == 16:
        Nk = 4  # 4 kata (128 bit)
        Nr = 10  # 10 rounds
    elif key_bytes == 24:
        Nk = 6  # 6 kata (192 bit)
        Nr = 12  # 12 rounds
    elif key_bytes == 32:
        Nk = 8  # 8 kata (256 bit)
        Nr = 14  # 14 rounds
    else:
        raise ValueError("Key size must be 16, 24, or 32 bytes")
        
    flat_s_box = {}
    for i in range(16):
        for j in range(16):
            byte_value = (i << 4) | j
            flat_s_box[byte_value] = s_box[i][j]
    
    def sub_word(word):
        return [flat_s_box[b] for b in word]
    
    def rot_word(word):
        return word[1:] + word[:1]
    

    key_schedule_words = 4 * (Nr + 1)
    

    key_as_words = []
    for i in range(0, key_bytes, 4):
        word = key[i:i+4]
        key_as_words.append(list(word))
    

    expanded_key_words = key_as_words.copy()
    

    for i in range(Nk, key_schedule_words):
        temp = list(expanded_key_words[i-1])
        
        if i % Nk == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= Rcon[i // Nk]
        elif Nk > 6 and i % Nk == 4:
            temp = sub_word(temp)

        new_word = []
        for j in range(4):
            new_word.append(expanded_key_words[i-Nk][j] ^ temp[j])
        
        expanded_key_words.append(new_word)
    
    round_keys = []
    for i in range(Nr + 1):
        round_key = []
        for row in range(4):
            round_key.append([expanded_key_words[i*4+col][row] for col in range(4)])
        round_keys.append(round_key)
    
    return round_keys