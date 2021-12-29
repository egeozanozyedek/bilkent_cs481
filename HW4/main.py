import argparse
from BLASTLike import BLASTLike


def main():

    parser = argparse.ArgumentParser(prog="CS481_HW3", description='Multiple Sequence Alignment!!!', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--ref', type=str, help='FASTA file containing the reference.')
    parser.add_argument('--qry', type=str, help='FASTA file containing the queries.')
    parser.add_argument('--k', type=int, help='Integer specifying the size of the k-mers.')
    parser.add_argument('--s', type=int, help='Integer specifying the score threshold for the high-scoring segment pairs.')


    args = parser.parse_args()

    ref_dir, qry_dir = args.ref, args.qry

    with open(ref_dir) as fasta:
        ref = fasta.read().split("\n", 1)[1].replace("\n", "")

    # there might be multiple sequences
    with open(qry_dir) as fasta:
        qry_list = [seq.split("\n", 1)[1].replace("\n", "") for seq in fasta.read().split(">")[1:]]

    print()

    for i, qry in enumerate(qry_list):
        a = BLASTLike(ref, qry, int(args.k), int(args.s), verbose=False)
        msp = a.align()
        msp_r_start = msp["r"][0] if msp else None
        print(f"Query Sequence {i + 1}: " + (f"{msp_r_start}\t(Additional Info: {msp})" if msp else f"No alignment found"))

    print()


if __name__ == '__main__':
    main()

