

from collections import deque


class Node:
    def __init__(self, index, key, depth):
        """
        Initializes node of tree
        :param index: Node ID
        :param key: the character that the node contains
        :param depth: the depth of the node in the tree, using this we can find lp(w)
        """
        self.index = index
        self.key = key
        self.children = list()
        self.fail_state = None
        self.end_word = None
        self.depth = depth

    def __str__(self):
        output = f", output: {self.end_word}" if self.end_word else ""
        return f"ID: {self.index}, Character:{self.key}, Children IDs: {[child.index for child in self.children]}, Fail State: " \
               f"{self.fail_state.index if self.fail_state else None}{output}"


class AhoCorasick:


    def __init__(self):
        """
        Initializes the needed components, such as the root, for the Aho Corasick search algorithm
        """
        self.root = Node(0, " ", 0)
        self.root.fail_state = self.root



    def build_trie(self, pattern_list):
        """
        Builds tree with a given list of pattern words
        :param word_list: Patterns
        """

        index = 0
        for pattern in pattern_list:  # insert each word into the tree, the index increases with each char inserted
            index = self._insert(self.root, pattern, pattern, index)

        self._assign_fail_states()  # assign fail states for all nodes



    def _insert(self, node, pattern, orig_pattern, index):
        """
        Inserts given word elements to the tree, sequentially
        :param node: The node from which the char will be inserted to
        :param word: The word, decreasing as new nodes are added
        :param orig_word: The unchanged word, needed for the last element to define it as a stop
        :param index: The node ID, index of the node
        :return: the accumulated index
        """

        # recursive stop, if the word has no elements left stop
        if pattern == "":
            node.end_word = orig_pattern
            return index

        #  get first char of pattern
        key = pattern[0]

        # initialize the next node as none
        next_node = None

        # if a node with the same key exists, continue with it
        for child in node.children:
            if child.key == key:
                next_node = child
                break

        # if there is not a node with the same char, create a new one
        if next_node is None:
            index += 1
            next_node = Node(index, key, node.depth + 1)
            node.children.append(next_node)

        return self._insert(next_node, pattern[1:], orig_pattern, index)



    def _assign_fail_states(self):
        """
        Assigns fail states, traversing in level order. Initializes the first two levels to have thier fail states as root
        """

        # create queue
        q = deque()

        # initialize
        for c in self.root.children:
            c.fail_state = self.root
            q.append((self.root, c.children))

        # while queue is not empty
        while q:

            # pop from queue
            parent, children = q.popleft()

            # find and assign the fail state
            for c in children:
                c.fail_state = self._find_fail_state(parent.fail_state, c)
                q.append((c, c.children))





    def _find_fail_state(self, fs, child):
        """
        Finds the fail state given the fail state of the parent and the child node. Simply jumps from fail state to fail state until root.
        :param fs: The fail state of the parent
        :param child: The child node
        :return: The fail state node
        """

        # if the fail state of the parent has a children with the same key, the fail state of the children node is the children of the fail state
        for c in fs.children:
            if child.key == c.key:
                return c

        # else if the fail state is the root, then assign the root
        if fs == self.root:
            return fs

        return self._find_fail_state(fs.fail_state, child)




    def __str__(self):
        info = self._str_helper(self.root)
        info = sorted(info.split("\n")[:-1], key=lambda x: int(x.split("ID: ")[1].split(",", 1)[0]))
        info = "\n".join(info)
        return info


    def _str_helper(self, node):
        """
        Helper function for print formatting
        :param node: Node to be printed
        :return: the node information in string
        """

        info = node.__str__() + "\n"

        for child in node.children:
            info += self._str_helper(child)

        return info


    def search(self, text):
        """
        Given a text string, uses the built tree to search for patterns. Follows the implementation in the slides.
        :param text: The text string to be searched
        :return: The indexes and the corresponding patterns
        """

        # initialize, i follows the text, j is the start of pattern, and current_node is the current ndoe
        current_node = self.root
        i = 0
        j = 0


        out = []

        # while text is remaining
        while i < len(text):

            # condition for the below while loop
            edge_exists = True

            while edge_exists:

                # check the children of current node to see if their key matches the char in text
                for child in current_node.children:

                    # if it does
                    if child.key == text[i]:

                        # and it is the end of the word, pass it to the output
                        if child.end_word is not None:
                            out.append((j, child.end_word))

                        # change the current node and increment
                        current_node = child
                        i += 1
                        break

                # if no break has occurred, meaning no matches, exit from the while loop and increment
                else:
                    edge_exists = False
                    i += 1

            # change current node to the fail state
            current_node = current_node.fail_state

            # change the start index to the fail states
            j = i - current_node.depth

        return out


