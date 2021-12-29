import logging
import numpy as np


class BLASTLike:
    """
    A BLAST Like alignment class that aligns given reference and query.
    """


    def __init__(self, reference, query, k, s, verbose=False):
        """
        Initialize the needed class members
        :param reference: The reference sequence
        :param query: The query sequence
        :param k: The kmer number (k length sequences will be considered)
        :param s: The alignment score threshold
        :param verbose: For debugging purposes
        """

        self.ref = reference
        self.qry = query
        self.k = k
        self.tresh = s
        self.hash_table = dict()
        self.q = 2 ** 31 - 1  # this is the max int value for 32-bit computers. It's used in hashing

        if verbose:
            logging.basicConfig(format="(%(asctime)s) %(message)s", datefmt="%H:%M:%S.%s", level=logging.DEBUG)\



    def _hash(self, kmer):
        """
        The hashing function. Uses the hashing function of Rabin-Karp
        :param kmer: The kmer to be hashed
        :return: the hash value
        """

        kmer = kmer.translate(str.maketrans({'A': '0', 'C': '1', 'G': '2', 'T': '3'}))
        hash_value = 0

        for i in range(self.k):
            hash_value = (hash_value + int(kmer[i]) * (4 ** (self.k - i - 1))) % self.q

        return str(int(hash_value))



    def _build_hash_table(self):
        """
        Function which builds the hash table for all kmers in the reference genome
        """

        for i in range(len(self.ref) - self.k + 1):
            try:
                self.hash_table[self._hash(self.ref[i:i + self.k])] += f" {i}"
            except KeyError:
                self.hash_table[self._hash(self.ref[i:i + self.k])] = f"{i}"



    def _find_match_indices(self):
        """
        Finds the indices where the kmers in the query match with the kmers in the reference. Uses the hash table to find near matches, and then
        solidifies the match by checking if they are equal
        :return: The match indices
        """

        matches = dict()

        for i in range(len(self.qry) - self.k + 1):

            qry_hash = self._hash(self.qry[i:i + self.k])
            if qry_hash in self.hash_table.keys():
                matches[i] = [int(v) for v in self.hash_table[qry_hash].split(" ") if self.ref[int(v):int(v)+self.k] == self.qry[i:i+self.k]]

        return matches



    def _seed_and_extend(self, match_score=1, mismatch_penalty=-1):
        """
        Seed and extend strategy. Here, we extend from both left and right the matched segments to find a longer high scoring segment.
        :param match_score: The match score, which is 1 by default
        :param mismatch_penalty: The mismatch penalty, which is -1 by default
        :return: A list that contains all high scoring segments
        """

        # start by doing the needed hashing and matching operations
        self._build_hash_table()
        matches = self._find_match_indices()
        logging.debug(matches)

        HSP = []

        # For all query indices, and the reference index lists that correspond to them
        for qry_i, ref_inds in zip(matches.keys(), matches.values()):
            for ref_i in ref_inds:

                current_score = self.k * match_score  # we know this since we check for exact match in the previous function _find_match_indices
                qry_j = qry_i + self.k - 1
                ref_j = ref_i + self.k - 1

                # we dont want to go out of border
                left_border = True if (qry_i and ref_i) > 0 else False
                right_border = True if (ref_j < len(self.ref) - 1) and (qry_j < len(self.qry) - 1) else False

                # while in between borders
                while left_border or right_border:

                    new_score = current_score
                    new_qry_i, new_ref_i = qry_i, ref_i
                    new_qry_j, new_ref_j = qry_j, ref_j


                    # extend left, compare the characters, add score
                    if left_border:
                        new_qry_i -= 1
                        new_ref_i -= 1

                        if self.qry[new_qry_i] == self.ref[new_ref_i]:
                            new_score += match_score
                        else:
                            new_score += mismatch_penalty


                    # extend right, compare the characters, add score
                    if right_border:
                        new_qry_j += 1
                        new_ref_j += 1

                        if self.qry[new_qry_j] == self.ref[new_ref_j]:
                            new_score += match_score
                        else:
                            new_score += mismatch_penalty


                    # if decreasing, stop extending and break
                    if current_score > new_score:
                        break

                    else:
                        qry_i, ref_i = new_qry_i, new_ref_i
                        qry_j, ref_j = new_qry_j, new_ref_j
                        current_score = new_score
                        left_border = True if (qry_i and ref_i) > 0 else False
                        right_border = True if (ref_j < len(self.ref) - 1) and (qry_j < len(self.qry) - 1) else False


                # if the score after seed and extend is higher than the threshold, add it to the HSP list if its a unique pair
                if current_score >= self.tresh:
                    pair = {"q": (qry_i, qry_j + 1), "r": (ref_i, ref_j + 1), "score": current_score}
                    if pair not in HSP:
                        HSP.append(pair)

        logging.debug(HSP)

        return HSP



    def align(self, match=1, mismatch=-1, gap=-0.5):
        """
        Needleman-Wunsch alignment after doing seed and extend. All the high scoring segment list for a single query get aligned, and the maximum
        scored one is taken to be the general alignment.
        :param match: The match score, which is 1 by default
        :param mismatch: The mismatch penalty, which is -1 by default
        :param gap: The gap penalty, which is -0.5 by default
        :return: The general alignment for the query, contains the start and end indexes for the query and reference, as well as the score
        """

        HSP = self._seed_and_extend()

        max_scoring_pair = None
        max_score = None

        # for all high scoring segment pairs in this query
        for pair in HSP:

            # obtain segments using the indices
            qry_seg = self.qry[pair["q"][0]:pair["q"][1]]
            ref_seg = self.ref[pair["r"][0]:pair["r"][1]]

            logging.debug(f"{qry_seg}, {ref_seg}")

            # create the DP matrix
            V = np.zeros(shape=(len(qry_seg) + 1, len(ref_seg) + 1))
            M, N = V.shape

            # initialize first row/column
            for i in range(V.shape[0] - 1):
                V[i + 1, 0] = gap + V[i, 0]
            for j in range(V.shape[1] - 1):
                V[0, j + 1] = gap + V[0, j]


            # this block builds the DP matrix
            for i in range(1, M):
                for j in range(1, N):

                    # chose the optimal direction
                    dp_decision = np.asarray([V[i - 1, j - 1] + (match if qry_seg[i - 1] == ref_seg[j - 1] else mismatch),
                                              V[i - 1, j] + gap,
                                              V[i, j - 1] + gap])

                    # make decision: down, diag, right?
                    decision = np.argmax(dp_decision)

                    # build the array
                    V[i, j] = dp_decision[decision]


            # the score is at the bottom right of the matrix
            score = V[-1, -1]

            # this whole part is so that the max scored pair is chosen
            if max_score is None or score > max_score:
                max_scoring_pair = pair
                max_scoring_pair["score"] = score
                max_score = score


        logging.debug(f"{max_scoring_pair}")

        return max_scoring_pair
