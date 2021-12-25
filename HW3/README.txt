This is my submission for HW3 of course CS481.

This homework requires the implementation of sequence to profile multiple sequence alignment. This folder contains 2 python scripts (MSA.py and
main.py), this README and a makefile, and finally 3 files for testing purposes in the testing subfolder.

A sample command would be as follows

    $python3 main.py --fasta testing/seq.fasta --aln testing/seqs.aln --out testing/out.txt --match 1 --mismatch -1 --gap -2

A short explanation of the python scripts are as follows:

main.py: This script obtains all inputs from the user, opens all needed files and reads/processes all required information to then pass it off to the
    MultipleSequenceAlignment class. After the optimal solution is built, the solution, as well as the input alignments are written to a text file
    (out.txt). Thats basically it, similar to all previous homeworks in its purpose.

MSA.py: This script contains the implementation of MultipleSequenceAlignment (MSA). There are three important points to touch on its
    implementation. Also, the implementation follows the explanation of sequence to profile alignment that is presented in the course slides.

        * Initializations: Perhaps the most important part of MSA is the initialization phase. In here, general needed initializations for the class
            are made, but more importantly we create the frequency matrix, which is the representation of the profile. For this assignment, and for
            bioinformatics, the alphabet is "ACGT-", where "-" represents a gap. The frequencies are found by adding up the # of occurences of the
            char y in the jth column. This gives us freq_matrix[i, j], where y = alphabet[i]. After this, the dynamic programming matrix, V, and the
            rebuild matrix (more on that later) are initialized. The initialization follows the one in the slides.


        * Dynamic Programming/Alignment: Here we align the given sequence according to the given profile. Its no different than any other DP
            implementation, we build V by following the msa scoring (which uses the frequency matrix) and the regular scoring (with the given penalty
            values) functions. This gives us V. Additionally, while we are building V, we also build the rebuild matrix, which contains the letters
            "u" for up, "d" for diagonal and "l" for left. This helps us find where to go in the building stage of the optimal sequence.

        * Building the optimal sequence: As it was mentioned, we store the move direction of the optimal path with "u", "d" and "l". After building
            the DP matrix (and the rebuild matrix), we create the optimal sequence following it. If its "l" then a gap is inserted into the optimal
            sequence. If its "d" or "u" (since we have no control over the profile) we insert the sequence char at seq[i]. This concludes MSA.