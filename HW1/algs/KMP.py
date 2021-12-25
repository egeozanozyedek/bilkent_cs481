class KnuthMorrisPratt(object):


    def __init__(self, T, P):

        self.text, self.query, self.text_size, self.query_size = T, P, len(T), len(P)
        self.FF, self.count = self.create_failure_function()

    def __call__(self):

        n, m = self.text_size, self.query_size
        i, j = 0, 0
        pos = []

        while i < n:

            if self.text[i] == self.query[j]:
                if j == m-1:
                    pos.append(i - j + 1)
                    i += 1
                    j = self.FF[j - 1]
                else:
                    i += 1
                    j += 1
            else:
                if j > 0:
                    j = self.FF[j-1]
                else:
                    i = i + 1
                    j = 0

            self.count += 1

        return pos, self.count


    def create_failure_function(self):
        m = self.query_size
        count = 0
        F, i, j = [0]*m, 1, 0

        while i < m:
            if self.query[i] == self.query[j]:
                F[i] = j+1
                i += 1
                j += 1
            elif j > 0:
                j = F[j - 1]
            else:
                F[i] = 0
                i += 1
            count += 1

        return F, count

