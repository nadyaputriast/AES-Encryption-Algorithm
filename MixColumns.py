def mix_columns(state):
    result = [row[:] for row in state]
    #multiplication GF(2^8)
    def mul_by_2(val):
        #multiplication 2 GF(2^8)
        if val & 0x80:
            return ((val << 1) ^ 0x1B) & 0xFF 
        else:
            return (val << 1) & 0xFF
    
    def mul_by_3(val):
        #multiplication 3 is equivalent to (2*val) XOR val
        return mul_by_2(val) ^ val
    
    for c in range(len(state[0])):
        s0 = (mul_by_2(state[0][c]) ^ mul_by_3(state[1][c]) ^ 
              state[2][c] ^ state[3][c])
        
        s1 = (state[0][c] ^ mul_by_2(state[1][c]) ^ 
              mul_by_3(state[2][c]) ^ state[3][c])
        
        s2 = (state[0][c] ^ state[1][c] ^ 
              mul_by_2(state[2][c]) ^ mul_by_3(state[3][c]))
        
        s3 = (mul_by_3(state[0][c]) ^ state[1][c] ^ 
              state[2][c] ^ mul_by_2(state[3][c]))
        
        #perbarui state
        result[0][c] = s0
        result[1][c] = s1
        result[2][c] = s2
        result[3][c] = s3
    
    return result