'''
INPUT: Numpy array 4x4 (state matrix) of integers from sub_bytes

OUTPUT: Numpy array 4x4 (state matrix) of integers 
'''

import numpy as np

def shift_rows(state): 
#First row remains unshifted 
    state[1] = np.roll(state[1],-1) #Second row shifts 1 to the left 
    state[2] = np.roll(state[2],-2) #Third row shifts 2 to the left 
    state[3] = np.roll(state[3],-3) #Fourth row shifts 3 to the left 

    return state.T.flatten()  #Transpose and flatten matrix



