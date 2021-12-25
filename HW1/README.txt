This is my code submission for the 1st HW assignment of CS 481.

The code consists of 4 python files (+ an __init__ file that is not important and just creates a python directory for the algorithms):

main.py: Creates a program for string matching that the user can input the desired text and query directories and the selected algorithm to.
It uses no external libraries. To convert the FASTA files into string objects, I used vanilla python to skip the first line and obtain the
sequence/text. I replace "\n" (newline) with an empty string to obtain a single line string at the end. After that, there are just many if statements
and print lines to present information to the user.

BF.py: The file which contains the BruteForce algorithm. Its pretty simple, checks whether the substring (i, i+m) in the text is the same as the
query. This might actually run faster than the other algorithms in simple text matching tasks.

KMP.py: KnuthMorrisPratt algorithm. Using a failure function, decreases the amount of comparisons by jumping more than a single character. The
comparisons are from left to right (j: 0 -> m).

BM.py: BoyerMoore algorithm. Uses the bad character rule/table to jump more than a single character, similar to KMP. Different than KMP, BM compares
right to left (j: m -> 0). This way less comparisons are required. This decreases search time for more complex tasks.