class BruteForce(object):

    def __call__(self, T, P):
        n, m = len(T), len(P)
        pos = []
        count = 0

        for i in range(0, n-m+1):
            if T[i:i + m] == P:
                pos.append(i + 1)
            count += m

        return pos, count
