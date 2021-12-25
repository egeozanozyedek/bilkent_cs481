import argparse
import numpy as np
from MSA import MultiSequenceAlignment as MSA


parser = argparse.ArgumentParser(prog="CS481_HW3", description='Multiple Sequence Alignment!!!', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--fasta', type=str, help='Input file.')
parser.add_argument('--aln', type=str, help='Alignment file.')
parser.add_argument('--out', type=str, help='Output file.')
parser.add_argument('--match', type=int, help='Match score')
parser.add_argument('--mismatch', type=int, help='Mismatch penalty.')
parser.add_argument('--gap', type=int, help='Gap penalty.')


args = parser.parse_args()

fasta_dir, aln_dir, out_dir, scoring = args.fasta, args.aln, args.out, (args.match, args.mismatch, args.gap)

with open(fasta_dir) as fasta, open(aln_dir) as aln:
    sequence = fasta.read().split("\n", 1)[1].replace("\n", "")
    profile_raw = aln.read()
    profile = np.asarray([list(x.split(" ", 1)[1]) for x in profile_raw.split("\n")])



MSA = MSA(scoring, profile, sequence)
aligned_seq = MSA.build()

print(profile_raw)
print("sequence " + aligned_seq)

with open(out_dir, "w") as out:
    out.write(profile_raw)
    out.write("\nsequence " + aligned_seq)
    out.close()


