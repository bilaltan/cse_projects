from RandomGenerator import RandomGenerator

class File:
    def __init__(self,line_count,dna_length_count,random_generator):
        self.line_count = line_count
        self.dna_length_count = dna_length_count
        self.dna = []
        self.random = random_generator

    def create_dna(self):
        count = 0
        while (count < self.line_count):
            dna_piece = ""
            piece_count = 0
            while(piece_count < self.dna_length_count):
                dna_piece += self.random.get_random_nucleotide()
                piece_count += 1
            self.dna.append(dna_piece)
            count += 1
        return self.dna
    