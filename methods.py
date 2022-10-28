import heapq


def AGP(func, a, b, r):
    x = [a, b]
    t = 1
    M = 0
    indM = 1
    indNew = 1
    z_opt_prev = min(func(a), func(b))
    R = []
    while x[t] - x[t-1] > 1e-4:
        z = list(map(func, x))

        changedM = False
        if indNew == indM:
            changedM = True
            for i in range(1, len(x)):
                tmpM = funcM(x[i-1], x[i], z[i-1], z[i])
                if tmpM > M:
                    M = tmpM
                    indM = i
        else:
            for i in range(indNew, indNew+2):
                tmpM = funcM(x[i - 1], x[i], z[i - 1], z[i])
                if tmpM > M:
                    changedM = True
                    M = tmpM
                    indM = i
        m = r * M if M > 0 else 1

        z_opt = min(z)
        if not changedM and z_opt == z_opt_prev:
            R.pop(indNew-1)
            for i in range(indNew, indNew+2):
                tmpR = funcR(m, z_opt, x[i-1], x[i], z[i-1], z[i])
                R.insert(i-1, tmpR)
        else:
            R = []
            for i in range(1, len(x)):
                tmpR = funcR(m, z_opt, x[i-1], x[i], z[i-1], z[i])
                R.append(tmpR)  # heapq.heappush(R, (i, tmpR))
        t = R.index(max(R))+1
        z_opt_prev = z_opt

        x_new = (x[t] + x[t-1]) / 2 - (z[t] - z[t-1]) / (2 * m)
        x.append(x_new)
        x.sort()
        indNew = x.index(x_new)
    return x


def funcM(x1, x2, z1, z2):
    return abs((z2 - z1) / (x2 - x1))


def funcR(m, z_opt, x1, x2, z1, z2):
    return m * (x2 - x1) + ((z2 - z1) ** 2) / (m * (x2 - x1)) - 2 * (z2 + z1 - 2 * z_opt)
