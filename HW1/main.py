import argparse
from algs import BruteForce, KnuthMorrisPratt, BoyerMoore
from datetime import datetime


parser = argparse.ArgumentParser(prog="CS481_HW1", description='String Matching!!!', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-i', type=str, help='Path of FASTA file to be queried.')
parser.add_argument('-o', type=str, help='Path of FASTA file containing query.')
parser.add_argument('-a', type=str, help='Algorithm selection. 4 options are available:'
                                         '\nBF: Standard Brute Force'
                                         '\nKMP: Knuth-Morris-Pratt Algorithm '
                                         '\nBM: Boyer-Moore'
                                         '\nA: To run all specified algorithms above.')
args = parser.parse_args()

text_dir = args.i
query_dir = args.o
selection = args.a


if selection not in ["A", "BF", "KMP", "BM"]:
    parser.error("Invalid algorithm selection. Use help for information on available algorithms.")


with open(text_dir) as text, open(query_dir) as query:

    T = text.read().split("\n", 1)[1].replace("\n", "")
    P = query.read().split("\n", 1)[1].replace("\n", "")


c_list = []
t_list = []
a_list = ["Brute Force", "Knuth-Morris-Pratt", "Boyer-Moore"]
not_matched = "The query was not found in given text."
matched = "The query was found in position(s): "

if selection == "BF" or selection == "A":

    s = datetime.now()
    pos, count = BruteForce()(T, P)
    e = datetime.now()
    time = (e - s).microseconds
    print(f"\n\n---- Brute Force ----\nComparisons: {count}.\nRuntime: {time} ms.\n"
          + (not_matched if len(pos) == 0 else (matched + str(pos)[1:-1])))

    c_list.append(count)
    t_list.append(time)

if selection == "KMP" or selection == "A":

    s = datetime.now()
    pos, count = KnuthMorrisPratt(T, P)()
    e = datetime.now()
    time = (e - s).microseconds
    print(f"\n\n---- Knuth-Morris-Pratt ----\nComparisons: {count}.\nRuntime: {time} ms.\n"
          + (not_matched if len(pos) == 0 else (matched + str(pos)[1:-1])))

    c_list.append(count)
    t_list.append(time)

if selection == "BM" or selection == "A":


    s = datetime.now()
    pos, count = BoyerMoore(T, P)()
    e = datetime.now()
    time = (e - s).microseconds
    print(f"\n\n---- Boyer-Moore ----\nComparisons: {count}.\nRuntime: {time} ms.\n"
          + (not_matched if len(pos) == 0 else (matched + str(pos)[1:-1])))

    c_list.append(count)
    t_list.append(time)


if selection == "A":

    c_best_ind = c_list.index(min(c_list))
    t_best_ind = t_list.index(min(t_list))

    print(f"\n\nThe best algorithm in terms of minimum time is {a_list[t_best_ind]} with {t_list[t_best_ind]} ms, "
          f"and in terms of minimum comparison is {a_list[c_best_ind]} with {c_list[c_best_ind]} characters compared.")


print("\n")
