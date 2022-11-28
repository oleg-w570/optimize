import queue


def AGP(func, a, b, r):
    Q = queue.PriorityQueue()
    interval_t = (a, b, func(a), func(b))  # interval[0] = x0, interval[1] = x1, interval[2] = z0, interval[3] = z1
    M = r * funcM(interval_t)
    z_opt_prev = 0
    while interval_t[1] - interval_t[0] > 1e-4:
        x_new = (interval_t[1] + interval_t[0]) / 2 - (interval_t[3] - interval_t[2]) / (2 * M)
        z_opt = func(x_new)
        newIntervals = ((interval_t[0], x_new, interval_t[2], z_opt), (x_new, interval_t[1], z_opt, interval_t[3]))

        changedM = False
        for interval in newIntervals:
            tmpM = r * funcM(interval)
            if tmpM > M:
                M = tmpM
                changedM = True

        if changedM or abs(z_opt - z_opt_prev) > 1e-8:
            tmpQ = queue.PriorityQueue()
            while not Q.empty():
                interval = Q.get()[1]
                tmpR = funcR(M, z_opt, interval)
                tmpQ.put((-tmpR, interval))
            Q = tmpQ
        for interval in newIntervals:
            tmpR = funcR(M, z_opt, interval)
            Q.put((-tmpR, interval))

        interval_t = Q.get()[1]
        z_opt_prev = z_opt

    x = [a]
    z = [func(a)]
    while not Q.empty():
        interval = Q.get()[1]
        x.append(interval[1])
        z.append(interval[3])
    return x, z


def funcM(interval):
    return abs((interval[3] - interval[2]) / (interval[1] - interval[0]))


def funcR(m, z_opt, interval):
    return m * (interval[1] - interval[0]) + ((interval[3] - interval[2]) ** 2) / (m * (interval[1] - interval[0])) - 2 * (interval[3] + interval[2] - 2 * z_opt)
