import argparse
import numpy as np



"""

Move through the ref from (0, k-1) to (1, k) to ... Add the start index of each kmer into a dict (key is the kmer and value is a list that cont
appends indices as the kmers are found). 

"""

def read_fasta(fasta_dir):
    with open(fasta_dir) as fasta:
        sequence = fasta.read().split("\n", 1)[1].replace("\n", "")


def main():

    parser = argparse.ArgumentParser(prog="CS481_HW3", description='Multiple Sequence Alignment!!!', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--ref', type=str, help='FASTA file containing the reference.')
    parser.add_argument('--qry', type=str, help='FASTA file containing the queries.')
    parser.add_argument('--k', type=int, help='Integer specifying the size of the k-mers.')
    parser.add_argument('--s', type=int, help='Integer specifying the score threshold for the high-scoring segment pairs.')


    args = parser.parse_args()

    fasta_dir, aln_dir, out_dir, scoring = args.fasta, args.aln, args.out, (args.match, args.mismatch, args.gap)

    MSA = MSA(scoring, profile, sequence)
    aligned_seq = MSA.build()

    print(profile_raw)
    print("sequence " + aligned_seq)

    with open(out_dir, "w") as out:
        out.write(profile_raw)
        out.write("\nsequence " + aligned_seq)
        out.close()


if __name__ == '__main__':
    main()

