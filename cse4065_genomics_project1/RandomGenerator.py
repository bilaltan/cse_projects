import random
import numpy as np

class RandomGenerator:

    nucleotides = ['A',"T","G","C"]
    def __init__(self, motif):
        self.motif = motif
    
    def get_random_nucleotide(self):
        return random.choice(self.nucleotides)

    def get_position(self,motif_length,num_mutations):
        return random.sample(range(0,motif_length), num_mutations)
    
    def get_index(self,probs):
        index = np.random.choice(np.arange(0, len(probs)), p=probs)
        return index

    def get_random_motif(self, motif_matrix):
        return random.randint(0,len(motif_matrix) - 1)