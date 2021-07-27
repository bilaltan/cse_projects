import numpy as np

class GibbsSampler:
    def __init__(self, dna, random_generator):
        self.dna = dna
        self.random_generator = random_generator

    def search(self, motif_length, n):
        matrix = self.get_random_motif(motif_length)
        temp_motif_matrix = matrix
        count = self.motif_count(motif_length)
        all_scores = self.motif_score(count=count)

        counter = 0
        changed = False
        while True:

            random_motif = self.random_generator.get_random_motif(matrix)
            ## TODO: IMPLEMENT
            count = self.remove_motif(count, matrix[random_motif])

            for i in range(len(count)):
                for j in range(len(count[i])):
                    count[i][j] += 1

            profile_matrix = self.profile_creation(count)
            # TODO : IMPLEMENT 
            matrix[random_motif] = self.motifs_from_gibbs(profile_matrix, self.dna.dna_string, motif_length, random_motif)
            
            count = self.motif_count(motif_length)
            new_motif_score = self.motif_score(count)

            # if new score is less than best score update best score
            if( all_scores > new_motif_score):
                temp_motif_matrix = matrix
                all_scores = new_motif_score
                changed = True

            counter += 1

            # if n is bigger than 0 run the algorithm with given iterations
            if ( n > 0):
                if (counter == n):
                    return temp_motif_matrix, all_scores
            else:
                # check algorithm every 50 iterations
                if ( counter % 50 == 0):
                    # if best score did not improved then end the algorithm
                    if(changed == False):
                        return temp_motif_matrix, all_scores
                    
                    changed = False

    def get_random_motif(self, motif_length):
        temp_matrix = []
        pos = self.random_generator.get_position(
            len(self.dna.dna_string[0]) - motif_length, len(self.dna.dna_string))
        for i in range(len(self.dna.dna_string)):
            temp_matrix.append(
                self.dna.dna_string[i][pos[i]:pos[i]+motif_length])
        return temp_matrix

    def motif_count(self, motif_length):
        count = []
        for i in range(motif_length):
            col = []
            num_occurrences = []
            for motif in self.random_generator.motif:
                col.append(motif[i])

            num_occurrences.append(col.count('A'))
            num_occurrences.append(col.count('C'))
            num_occurrences.append(col.count('G'))
            num_occurrences.append(col.count('T'))

            count.append(num_occurrences)

        return count
    
    def motif_score(self, count):
        score = 0
        for i in count:
            score += sum(i) - max(i)
        return score

    
    def profile_creation(self, count):
        profile_matrix = []
        max_number = sum(count[0])
        for i in range(len(count)):
            probs = []
            for j in range(4):
                probs.append(count[i][j]/max_number)
            profile_matrix.append(probs)
        return profile_matrix

    
    def set_motif_for_gibbs(self,created_profile_matrix,motif_length):
        matrix = []
        for each_dna in self.dna.dna_string:
            probs = []
            for j in range(len(each_dna) - motif_length + 1):
                probs.append(self.motif_prob(created_profile_matrix, each_dna[j:j+motif_length], motif_length))
                
            index = probs.index(max(probs))
            matrix.append(each_dna[index: index + motif_length])
        
        return matrix
    
    
    def motif_prob(self,profile_matrix, motif, motif_length):
        prob = 1
        for i in range(len(motif)):
            if (motif[i] == 'A'):
                prob = prob * profile_matrix[i][0]
            elif (motif[i] == 'C'):
                prob = prob * profile_matrix[i][1]
            elif (motif[i] == 'G'):
                prob = prob * profile_matrix[i][2]
            elif (motif[i] == 'T'):
                prob = prob * profile_matrix[i][3]
        return prob
    
    def remove_motif(self,count, motif):
        for i in range(len(motif)):
            if (motif[i] == 'A'):
                count[i][0] -= 1
            if (motif[i] == 'C'):
                count[i][1] -= 1
            if (motif[i] == 'G'):
                count[i][2] -= 1
            elif (motif[i] == 'T'):
                count[i][3] -= 1
        return count
    
    def motifs_from_gibbs(self,profile_matrix, dna, motif_length, random_motif):
        probs = []
        for j in range(len(dna[random_motif]) - motif_length + 1):
            probs.append(self.motif_prob(profile_matrix, dna[random_motif][j:j+motif_length], motif_length))

        factor = 1/float(sum(probs))
        for i in range(len(probs)):
            probs[i] = probs[i] * factor

        index = self.random_generator.get_index(probs)
        return dna[random_motif][index: index + motif_length]
    
    def motif_prob(self,profile_matrix, motif, motif_length):
        prob = 1
        for i in range(len(motif)):
            if (motif[i] == 'A'):
                prob = prob * profile_matrix[i][0]
            elif (motif[i] == 'C'):
                prob = prob * profile_matrix[i][1]
            elif (motif[i] == 'G'):
                prob = prob * profile_matrix[i][2]
            elif (motif[i] == 'T'):
                prob = prob * profile_matrix[i][3]
        return prob
