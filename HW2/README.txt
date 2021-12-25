This is my submission for HW2 of course CS481.

The submission contains 2 python files and a makefile. There is also a text file, separate from this README, that is used for testing purposes
("dummy.txt").

A sample command line prompt to run the code would be as follows

        $python3 main.py -i mytestfile.txt

Now onto the explanations of the code.

main.py: This is the main file which uses argument parsing to obtain a text file as an input. The input is assumed to have two lines, the first one
    containing the patterns and the second line having the search text. These are seperated by "\n", so we split these and obtain them as separate
    variables. Then, the patterns are split by spaces and passed onto the AhoCorasick object to build the keyword trie. Then the output is printed
    (in the same format as the assignment).

AhoCorasick.py: This is where the AhoCorasick algorithm is implemented. There are three main points that needs to be discussed.

    * Building the trie: This is perhaps where most of the hard work went into. First a Node class was implemented. It has its children in a python
        list, its fail state as None initially and has some other identifiers such as the char it represents and its ID (index). This Node class is used
        by AhoCorasick (AC for this readme) as its trie elements. The constructor of AC assigns a class variable called root, which has 0 ID and " " as key.
        Then we build the tree, for each pattern in the pattern list, and for each char in the pattern, either a new node is created or an existing one is
        used. This is done recursively for each pattern. If the node contains the last char of pattern, then a variable "end_word" is assigned the original
        pattern. This is used in search. The ID of each node is assigned in the order they are created. After all patterns are added, the tree is built.
        Only thing remaining in this "pre-processing" stage is assigning the failure links.

    * Failure Links: The failure links are found after the building of the tree. The fail states of the first two depths (0 and 1) are assigned as the
        root. Then, in level order fashion, using a queue, each Nodes failure link is found. Node A's parent is Node PA, and Node PA's failure link is FS-PA.
        For A, first the parents' failure link is checked. If FS-PA has children that have the same key as A, then the failure link of A is that children.
        Else, this is retried for FS-FS-PA, which is the failure link of the failure link. So we jump until we are at the root, at which point we assign
        the root itself as the failure state of A.

    * Search: After the tree is fully built and failure states/links are assigned to each node, we move onto our actual goal. The search algorithm is
        implemented in the same way as it is in the slides. First we have two indexes i and j, i is the text pointer and j always points to the start of a
        pattern. Then, while an edge exists, or the node has a child that is the same as T[i], we loop and continue to increment i and go onto the next node.
        If a match is found, aka the end_word element of a Node is not none, then we pass the pattern and the index j into an output list. If a match is not
        found, we use the fail state of the node as the current node, and reset i to the start of the fail state pattern (i = j - lp(v)). This continues until
        all chars in the text are compared.

