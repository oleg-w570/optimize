def AGP(func, a, b, r, eps):
    k = 0
    x = [a, b]
    pairs_x = pairs(x)
    t = 0
    while pairs_x[t][1] - pairs_x[t][0] > eps:
        x.sort()
        z = list(map(func, x))
        pairs_x = pairs(x)
        pairs_z = pairs(z)
        M = max(map(funcM, pairs_x, pairs_z))
        m = r * M if M > 0 else 1
        R = list(map(funcR(m), pairs_x, pairs_z))
        t = R.index(max(R))
        x_new = (pairs_x[t][1] + pairs_x[t][0]) / 2 - (pairs_z[t][1] - pairs_z[t][0]) / (2 * m)
        x.append(x_new)
        k += 1
    opt = min(map(func, x))
    return opt, k


def pairs(lst):
    return [lst[i:i + 2] for i in range(0, len(lst) - 1)]


def funcM(pair_x, pair_z):
    return abs((pair_z[1] - pair_z[0]) / (pair_x[1] - pair_x[0]))


def funcR(m):
    def f(pair_x, pair_z):
        return m * (pair_x[1] - pair_x[0]) + ((pair_z[1] - pair_z[0]) ** 2) / (m * (pair_x[1] - pair_x[0])) - 2 * (
                    pair_z[1] + pair_z[0])
    return f
