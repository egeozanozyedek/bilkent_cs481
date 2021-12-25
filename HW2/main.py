import argparse
from AhoCorasick import AhoCorasick


parser = argparse.ArgumentParser(prog="CS481_HW2", description='Pattern Search!!!', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-i', type=str, help='Input file.')

args = parser.parse_args()

input_dir = args.i

with open(input_dir) as text:
    patterns, text = text.read().split("\n", 1)


ac = AhoCorasick()
ac.build_trie(patterns.split(" "))
output = ac.search(text)

build_str = ac.__str__()
search_str = "\n".join([f"{out[1]} found at index {out[0]}" for out in output])

out_str = f"\n--------------------------------BUILD TREE--------------------------------\n{build_str}\n" \
          f"\n--------------------------------SEARCH--------------------------------\n{search_str}"

print(out_str)
