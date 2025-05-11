'''
INPUT: Numpy array 4x4 (state matrix) of integers from add_round_key

OUTPUT: Numpy array 4x4 (state matrix) of integers 
'''

import numpy as np

def inv_shiftrows(state): 
#First row remains unshifted 
    state[1] = np.roll(state[1],1) #Second row shifts 1 to the right
    state[2] = np.roll(state[2],2) #Third row shifts 2 to the right  
    state[3] = np.roll(state[3],3) #Fourth row shifts 3 to the right 

    return state     
