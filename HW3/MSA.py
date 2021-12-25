import numpy as np


class MultiSequenceAlignment:

    def __init__(self, scoring, profile, sequence):
        """
        Initializes the frequency matrix, DP matrix (V) and the rebuild matrix. Also initializes some needed class variables.
        :param scoring: The scoring rules, match score, mismatch penalty and gap penalty inside a tuple.
        :param profile: The profile, a.k.a previously aligned sequences. The freq matrix is built accordingly.
        :param sequence: The sequence to be aligned following the profile.
        """

        # create class variables
        self.match, self.mismatch, self.gap = scoring
        M, N = len(sequence), profile.shape[1]
        self.sequence = sequence
        self.profile = profile

        # create the alphabet used in the alignments
        self.alphabet = ["A", "C", "G", "T", "-"]

        # create the frequency matrix
        self.freq_matrix = np.zeros(shape=(len(self.alphabet), N))

        for i, val in enumerate(self.alphabet):
            for j in range(N):
                self.freq_matrix[i, j] = (self.profile[:, j] == val).mean()

        # create the DP matrices, and initialize V. V is 1 dimension bigger in both axes.
        self.V = np.zeros(shape=(M + 1, N + 1))
        self.V[0, 0] = 0


        # initialize sequence axes, follows the slides
        for i in range(self.V.shape[0] - 1):
            self.V[i + 1, 0] = self._regular_score(self.sequence[i], "-") + self.V[i, 0]

        # initialize profile axes, follows the slides
        for j in range(self.V.shape[1] - 1):
            self.V[0, j + 1] = self._msa_score("-", j) + self.V[0, j]




    def build(self):
        """
        Builds the optimal aligned sequence according to the given profile.
        :return: The optimal alignment, DP solution
        """

        # first, create the DP matrix V, a.k.a align the sequence to the profile
        rebuild = self._align()

        # start from bottom right of the matrix, initialize the aligned sequence
        i, j = rebuild.shape
        i -= 1
        j -= 1
        aligned_sequence = ""

        # up until we reach the top left
        while i >= 0 and j >= 0:

            # if diagonal, match/mismatch, go diagonal (i - 1, j - 1)
            if rebuild[i, j] == "d":
                aligned_sequence = self.sequence[i] + aligned_sequence
                i -= 1
                j -= 1

            # if left, insert gap, go left (i, j - 1)
            elif rebuild[i, j] == "l":
                aligned_sequence = "-" + aligned_sequence
                j -= 1

            # if up, gap to the profile (aka do not change the sequence), go up (i - 1, j)
            elif rebuild[i, j] == "u":
                aligned_sequence = self.sequence[i] + aligned_sequence
                i -= 1
            else:
                raise Exception("How did that happen? I'm sure this is impossible, but just in case...")

        return aligned_sequence



    def _regular_score(self, x, y):
        """
        The delta score function, returns the alignment score between two chars
        :param x: the character x to be aligned with y
        :param y: the character y to be aligned with x
        :return: the match/mismatch/gap score
        """


        if x == "-" or y == "-":
            return self.gap
        elif x == y:
            return self.match

        else:
            return self.mismatch



    def _msa_score(self, x, j):
        """
        The multiple seq alignment score function, multiplies the frequency of score between x and y with the freq of y at the jth column.
        :param x: The char x for which the alignment score is to be found
        :param j: Column number of the profile
        :return: Score
        """

        score = 0
        for y in self.alphabet:
            score += self._regular_score(x, y) * self.freq_matrix[self.alphabet.index(y), j]

        return score


    def _align(self):
        """
        Builds the DP matrix V row by row. It follows the scoring given in the slides. Also builds the rebuild matrix with directions as its elements.
        :return: the rebuild matrix to build the optimal alignment
        """

        M, N = self.V.shape
        direction = ["d", "u", "l"]
        rebuild = np.full(shape=(M - 1, N - 1), fill_value="")

        for i in range(1, M):
            for j in range(1, N):

                k, z = i - 1, j - 1
                seq_k = self.sequence[k]

                # chose the optimal direction
                dp_decision = np.asarray([self.V[i - 1, j - 1] + self._msa_score(seq_k, z),
                                          self.V[i - 1, j] + self._regular_score(seq_k, "-"),
                                          self.V[i, j - 1] + self._msa_score("-", z)])

                # make decision: down, diag, right?
                decision = np.argmax(dp_decision)

                # build the arrays
                self.V[i, j] = dp_decision[decision]
                rebuild[k, z] = direction[decision]

        return rebuild

