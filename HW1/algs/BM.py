class BoyerMoore(object):

    def __init__(self, T, P):

        self.text, self.query, self.text_size, self.query_size = T, P, len(T), len(P)
        self.bct = self.create_bad_char_table()


    def __call__(self):

        n, m = self.text_size, self.query_size
        i, j = 0, m - 1
        pos = []
        count = 0

        while i < n - m + 1:

            if self.text[i + j] == self.query[j]:
                if j == 0:
                    pos.append(i + 1)
                    if i + m < n:
                        j = m - 1
                        i += self.calculate_shift(i, j)

                    else:
                        break
                else:
                    j -= 1
            else:
                i += self.calculate_shift(i, j)
                j = m - 1

            count += 1

        return pos, count


    def calculate_shift(self, i, j):

        bc_shift = self.bct.get(self.text[i + j], self.query_size)
        return max(bc_shift, 1)


    def create_bad_char_table(self):

        bad_char_table = {}

        for i in range(self.query_size):
            bad_char_table[self.query[i]] = self.query_size - 1 - i

        return bad_char_table








