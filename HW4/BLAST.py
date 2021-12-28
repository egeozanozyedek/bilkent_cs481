import logging
import re
import sys

import numpy as np


class BLAST:

    def __init__(self, reference, query, k, s):
        self.ref = reference
        self.qry = query
        self.k = k
        self.tresh = s
        self.hash_table = dict()
        self.q = 2 ** 31 - 1

        logging.basicConfig(format="(%(asctime)s) %(message)s", datefmt="%H:%M:%S.%s", level=logging.DEBUG)
        logging.debug('This message should go to the log file')

        pass


    def _hash(self, kmer):

        kmer = kmer.translate(str.maketrans({'A': '0', 'C': '1', 'G': '2', 'T': '3'}))
        hash_value = 0

        for i in range(self.k):
            hash_value = (hash_value + int(kmer[i]) * (4 ** (self.k - i - 1))) % self.q



        return str(int(hash_value))


    def _build_hash_table(self):

        for i in range(len(self.ref) - self.k + 1):
            try:
                self.hash_table[self._hash(self.ref[i:i + self.k])] += f" {i}"
            except KeyError:
                self.hash_table[self._hash(self.ref[i:i + self.k])] = f"{i}"

        logging.debug(a.hash_table)


    def _find_match_indices(self):

        matches = dict()

        for i in range(len(self.qry) - self.k + 1):

            qry_hash = self._hash(self.qry[i:i + self.k])
            if qry_hash in self.hash_table.keys():
                matches[i] = [v for v in self.hash_table[qry_hash].split(" ") if self.ref[int(v):int(v)+self.k] == self.qry[i:i+self.k]]


        logging.debug(matches)

        #
        # for key, value in matches.items():
        #
        #     qi = key
        #     temp = list()
        #
        #     for i, v in enumerate(value):
        #         logging.debug(f"{i}, {v}, {qi}, {self.ref[v:v + self.k]}, {self.qry[qi:qi + self.k]}")
        #         if self.ref[v:v+self.k] == self.qry[qi:qi+self.k]:
        #             temp.append(v)
        #
        #     matches[key] = temp
        #
        #
        #
        # logging.debug(matches)

        return matches



    def seed_and_extend(self):
        pass


if __name__ == '__main__':

    with open("sequence.fasta") as fasta:
        ref = fasta.read().split("\n", 1)[1].replace("\n", "")

    with open("query.fasta") as fasta:
        qry = fasta.read().split("\n", 1)[1].replace("\n", "")

    # ref = "AGTCGTCACCTGGT"
    # qry = "CAC"
    a = BLAST(ref, qry, 32, -1)
    a._build_hash_table()
    m = a._find_match_indices()

