class RandomizedMotifSearch:
    def __init__(self, dna, random_generator):
        self.dna = dna
        self.random_generator = random_generator

    def search(self, motif_length):
        matrix = self.get_random_motif(motif_length)
        temp_motif_matrix = matrix
        count = self.motif_count(motif_length)
        all_scores = self.motif_score(count=count)
        while True:
            profile_matrix = self.create_profile(count)
            matrix = self.set_motif_for_randomized(profile_matrix,motif_length) 
            # get count matrix
            count = self.motif_count(motif_length)
            # calculate the score of new motif matrix
            new_motif_score = self.motif_score(count)
            if( all_scores > new_motif_score):
                temp_motif_matrix = matrix
                all_scores = new_motif_score
        # if there is improvment than stop algorithm
            else:
                return temp_motif_matrix, all_scores

    def get_random_motif(self, motif_length):
        temp_matrix = []
        pos = self.random_generator.get_position(
            len(self.dna.dna_string[0]) - motif_length, len(self.dna.dna_string))
        for i in range(len(self.dna.dna_string)):
            temp_matrix.append(
                self.dna.dna_string[i][pos[i]:pos[i]+motif_length])
        return temp_matrix
    # TODO: Change it

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
    # TODO: Change it

    def motif_score(self, count):
        score = 0
        for i in count:
            score += sum(i) - max(i)

        return score
    #TODO: Change it
    def create_profile(self, count):
        profile_matrix = []
        max_number = sum(count[0])
        for i in range(len(count)):
            probs = []
            for j in range(4):
                probs.append(count[i][j]/max_number)
            profile_matrix.append(probs)
        return profile_matrix
    #TODO: Change it
    def set_motif_for_randomized(self,created_profile_matrix,motif_length):
        matrix = []
        for each_dna in self.dna.dna_string:
            probs = []
            for j in range(len(each_dna) - motif_length + 1):
                x=self.motif_prob(profile_matrix = created_profile_matrix, motif=each_dna[j:j+motif_length])
                probs.append(x)
                
            index = probs.index(max(probs))
            matrix.append(each_dna[index: index + motif_length])
        
        return matrix
    
    def motif_prob(self,profile_matrix, motif):
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

