class Mutation:
    def __init__(self,motif_length,random_generator):
        self.motif_length = motif_length
        self.random_generator = random_generator
        pass
    
    def create_mutations(self,mutation_count):
        length_motif = len(self.random_generator.motif)
        for motif_index in range(len(self.random_generator.motif)):
            pos_elements=self.random_generator.get_position(length_motif,mutation_count)
            self.random_generator.motif[motif_index] = list(self.random_generator.motif[motif_index])
            for pos in pos_elements:
                while True:
                    mutated_nucleoid_piece = self.random_generator.get_random_nucleotide()

                    if (self.random_generator.motif[motif_index][pos] != mutated_nucleoid_piece):
                        self.random_generator.motif[motif_index][pos] = mutated_nucleoid_piece
                        break
            self.random_generator.motif[motif_index] = "".join(self.random_generator.motif[motif_index])

    def mutate_dna(self,dna,positions,motif_length):
        length_motif = len(self.random_generator.motif)
        for motif_index in range(length_motif):
            dna.dna_string[motif_index] = list(dna.dna_string[motif_index])
            temp_index = positions[motif_index] + motif_length
            dna.dna_string[motif_index][positions[motif_index]:temp_index] = self.random_generator.motif[motif_index]
            dna.dna_string[motif_index] = "".join(dna.dna_string[motif_index])
        
                        

        
        