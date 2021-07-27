from GibbsSampler import GibbsSampler
from Logger import Logger
from RandomGenerator import RandomGenerator
from File import File
from DNA import DNA
from Mutation import Mutation
from RandomizedMotifSearch import RandomizedMotifSearch

def main():
    random_generator = RandomGenerator(['ACGTACGTAC'] * 10)

    file = File(dna_length_count=500,random_generator=random_generator,line_count=10)
    dna = DNA(file.create_dna())

    mutation = Mutation(10,random_generator=random_generator)
    mutation.create_mutations(4)
    mutation.mutate_dna(dna=dna,positions=random_generator.get_position(490,10),motif_length=10)

    test_randomized_search = RandomizedMotifSearch(dna, random_generator)
    best_motif,best_score=test_randomized_search.search(9)
    count = motif_count(best_motif,9)
    logger = Logger()
    logger.log_randomized(best_score=best_score,best_motif=best_motif,count=count)
    
    test_gibbs_search = GibbsSampler(dna,random_generator)
    best_motif,best_score=test_gibbs_search.search(9,0)

    count = motif_count(best_motif,9)
    logger = Logger()
    logger.log_gibbs(best_score=best_score,best_motif=best_motif,count=count)

    pass

def motif_count(motif_matrix, motif_length):
        count = []
        for i in range(motif_length):
            col = []
            num_occurrences = []
            for motif in motif_matrix:
                col.append(motif[i])
            num_occurrences.append(col.count('A'))
            num_occurrences.append(col.count('C'))
            num_occurrences.append(col.count('G'))
            num_occurrences.append(col.count('T'))

            count.append(num_occurrences)
        return count
main()