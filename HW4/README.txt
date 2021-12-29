This is my submission for HW4 of course CS481.

This homework requires the implementation of a BLAST like alignment tool. This folder contains 2 python scripts (BLASTLike.py and
main.py), this README and a makefile, and finally 2 FASTA files for testing purposes.

A sample command would be as follows

    $python3 main.py --ref sequence.fasta --qry query.fasta --k 11 --s 50

A short explanation of the python scripts are as follows:

main.py: This script obtains all inputs from the user, opens all needed files and reads/processes all required information to then pass it off to the
    BLASTLike class. After the needed operations and the alignment is done, the start index of the alignment is printed to standard output.

MSA.py: This script contains the implementation of BLASTLike. There are two important points to touch on its
    implementation.

        * Hashing and Finding Matching Indices: The implemented hash function is the same as the Rabin-Karp hash function. Using this, a hash table is
            built for all k-mer's in the reference sequence. Then, using this hash table, matches are found within the query by using the hash
            function for all the k-mer's in the query sequence. Then, these are transferred to seed and extend.

        * Seed ad Extend, and Alignment: First, the matches go through seed and extend (no gaps). Here, the matches are extended from left and right (if
            possible) until the score starts decreasing. After extending as much as possible, the highest scoring segment pairs are transferred to
            alignment. For alignment, the Needleman-Wunsch alignment is used. For each pair, the DP matrix is built and the maximum score out of all
            pairs is chosen as the general alignment of the query. Then the maximum scoring pair is returned.