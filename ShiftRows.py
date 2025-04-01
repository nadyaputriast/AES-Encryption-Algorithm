def shift_rows(state):
    result = [row[:] for row in state]    
    result[1] = result[1][1:] + result[1][:1]
    result[2] = result[2][2:] + result[2][:2]
    result[3] = result[3][3:] + result[3][:3]
    return result