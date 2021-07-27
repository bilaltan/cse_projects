class Logger:
    def __init__(self) -> None:
        pass

    def log_randomized(self, best_score, best_motif, count):
        print('\n')
        print('Randomized motif search with k = 9')
        print('\n')
        print('Best score: {}'.format(best_score))
        print('Best motifs:')
        for i in best_motif:print(i)
        print('\nConsensus string: {}'.format(self.consensus_sequence_generator(count)))
        print('\n')
        
    def log_gibbs(self, best_score, best_motif, count):
        print('\n')
        print('Gibbs sampler with k = 9')
        print('\n')
        print('Best score: {}'.format(best_score))
        print('Best motifs:')
        for i in best_motif:print(i)
        print('\nConsensus string: {}'.format(self.consensus_sequence_generator(count)))
        print('\n')

    def consensus_sequence_generator(self,count):
        consensus_sequence = ''
        for i in range(len(count)):
            max_element = max(count[i])
            for j in range(4):
                if ( count[i][j] == max_element ):
                    if (j == 0):
                        consensus_sequence = consensus_sequence + 'A/'
                    elif (j == 1):
                        consensus_sequence = consensus_sequence + 'C/'
                    elif (j == 2):
                        consensus_sequence = consensus_sequence + 'G/'
                    elif (j == 3):
                        consensus_sequence = consensus_sequence + 'T/'
            
            consensus_sequence = consensus_sequence[0:len(consensus_sequence) -1]
            consensus_sequence = consensus_sequence + ' ' 
        return consensus_sequence

        