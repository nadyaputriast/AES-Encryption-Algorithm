def add_round_key(state, round_key):
    result = [row[:] for row in state]
    
    for i in range(4):
        for j in range(4):
            result[i][j] = state[i][j] ^ round_key[i][j]
    return result