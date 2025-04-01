from tabel import tabel

def sub_bytes(state):
    s_box, Rcon = tabel()
    flat_s_box = {}
    for i in range(16):
        for j in range(16):
            byte_value = (i << 4) | j 
            flat_s_box[byte_value] = s_box[i][j]
    result = [row[:] for row in state]
    

    for i in range(4):
        for j in range(4):
            result[i][j] = flat_s_box[state[i][j]]
    
    return result