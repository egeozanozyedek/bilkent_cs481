import logging
import re
import sys

import numpy as np


class BLASTLike:
    """

    """


    def __init__(self, reference, query, k, s, verbose=True):
        """

        :param reference:
        :param query:
        :param k:
        :param s:
        :param verbose:
        """
        self.ref = reference
        self.qry = query
        self.k = k
        self.tresh = s
        self.hash_table = dict()
        self.q = 2 ** 31 - 1

        if verbose:
            logging.basicConfig(format="(%(asctime)s) %(message)s", datefmt="%H:%M:%S.%s", level=logging.DEBUG)\



    def _hash(self, kmer):
        """

        :param kmer:
        :return:
        """

        kmer = kmer.translate(str.maketrans({'A': '0', 'C': '1', 'G': '2', 'T': '3'}))
        hash_value = 0

        for i in range(self.k):
            hash_value = (hash_value + int(kmer[i]) * (4 ** (self.k - i - 1))) % self.q

        return str(int(hash_value))



    def _build_hash_table(self):
        """

        :return:
        """

        for i in range(len(self.ref) - self.k + 1):
            try:
                self.hash_table[self._hash(self.ref[i:i + self.k])] += f" {i}"
            except KeyError:
                self.hash_table[self._hash(self.ref[i:i + self.k])] = f"{i}"



    def _find_match_indices(self):
        """

        :return:
        """

        matches = dict()

        for i in range(len(self.qry) - self.k + 1):

            qry_hash = self._hash(self.qry[i:i + self.k])
            if qry_hash in self.hash_table.keys():
                matches[i] = [int(v) for v in self.hash_table[qry_hash].split(" ") if self.ref[int(v):int(v)+self.k] == self.qry[i:i+self.k]]

        return matches



    def _seed_and_extend(self, match_score=1, mismatch_penalty=-1):
        """

        :param match_score:
        :param mismatch_penalty:
        :return:
        """

        self._build_hash_table()
        matches = self._find_match_indices()
        logging.debug(matches)

        HSP = []

        for qry_i, ref_inds in zip(matches.keys(), matches.values()):

            for ref_i in ref_inds:

                current_score = self.k * match_score
                qry_j = qry_i + self.k - 1
                ref_j = ref_i + self.k - 1

                left_border = True if (qry_i and ref_i) > 0 else False
                right_border = True if (ref_j < len(self.ref) - 1) and (qry_j < len(self.qry) - 1) else False


                while left_border or right_border:

                    new_score = current_score
                    new_qry_i, new_ref_i = qry_i, ref_i
                    new_qry_j, new_ref_j = qry_j, ref_j

                    if left_border:

                        new_qry_i -= 1
                        new_ref_i -= 1

                        if self.qry[new_qry_i] == self.ref[new_ref_i]:
                            new_score += match_score
                        else:
                            new_score += mismatch_penalty

                    if right_border:

                        new_qry_j += 1
                        new_ref_j += 1

                        if self.qry[new_qry_j] == self.ref[new_ref_j]:
                            new_score += match_score
                        else:
                            new_score += mismatch_penalty


                    # if decreasing
                    if current_score > new_score:
                        break

                    else:
                        qry_i, ref_i = new_qry_i, new_ref_i
                        qry_j, ref_j = new_qry_j, new_ref_j
                        current_score = new_score
                        left_border = True if (qry_i and ref_i) > 0 else False
                        right_border = True if (ref_j < len(self.ref) - 1) and (qry_j < len(self.qry) - 1) else False


                if current_score >= self.tresh:
                    pair = {"q": (qry_i, qry_j + 1), "r": (ref_i, ref_j + 1), "score": current_score}
                    if pair not in HSP:
                        HSP.append(pair)

        logging.debug(HSP)

        return HSP



    def align(self, match=1, mismatch=-1, gap=-0.5):
        """

        :param match:
        :param mismatch:
        :param gap:
        :return:
        """

        HSP = self._seed_and_extend()

        max_scoring_pair = None
        max_score = None

        for pair in HSP:

            qry_seg = self.qry[pair["q"][0]:pair["q"][1]]
            ref_seg = self.ref[pair["r"][0]:pair["r"][1]]
            V = np.zeros(shape=(len(qry_seg) + 1, len(ref_seg) + 1))
            M, N = V.shape

            logging.debug(f"{qry_seg}, {ref_seg}")

            V = np.zeros(shape=(len(qry_seg) + 1, len(ref_seg) + 1))

            for i in range(V.shape[0] - 1):
                V[i + 1, 0] = gap + V[i, 0]
            for j in range(V.shape[1] - 1):
                V[0, j + 1] = gap + V[0, j]

            for i in range(1, M):
                for j in range(1, N):


                    # chose the optimal direction
                    dp_decision = np.asarray([V[i - 1, j - 1] + (match if qry_seg[i - 1] == ref_seg[j - 1] else mismatch),
                                              V[i - 1, j] + gap,
                                              V[i, j - 1] + gap])

                    # make decision: down, diag, right?
                    decision = np.argmax(dp_decision)

                    # build the arrays
                    V[i, j] = dp_decision[decision]


            score = V[-1, -1]


            if max_score is None or score > max_score:
                max_scoring_pair = pair
                max_scoring_pair["score"] = score
                max_score = score


        logging.debug(f"{max_scoring_pair}")

        return max_scoring_pair
