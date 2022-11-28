import queue


class AGP:
    def __init__(self, func, a, b, r):
        self.func = func
        self.a = a
        self.b = b
        self.r = r
        self.Q = queue.PriorityQueue()
        self.niter = 0

    @staticmethod
    def calculateM(interval) -> float:
        return abs((interval[3] - interval[2]) / (interval[1] - interval[0]))

    @staticmethod
    def calculateR(m, z_opt, interval) -> float:
        return m * (interval[1] - interval[0]) + ((interval[3] - interval[2]) ** 2) / (
                    m * (interval[1] - interval[0])) - 2 * (interval[3] + interval[2] - 2 * z_opt)

    def get_result(self):
        x = [self.a]
        z = [self.func(self.a)]
        while not self.Q.empty():
            interval = self.Q.get()[1]
            x.append(interval[1])
            z.append(interval[3])
        return x, z, self.niter

    def clear(self):
        self.Q = queue.PriorityQueue()
        self.niter = 0

    def run(self):
        self.clear()
        interval_t = (self.a, self.b, self.func(self.a),
                      self.func(self.b))  # interval[0] = x0, interval[1] = x1, interval[2] = z0, interval[3] = z1
        M = self.r * self.calculateM(interval_t)
        z_opt_prev = 0
        while interval_t[1] - interval_t[0] > 1e-4:
            x_new = (interval_t[1] + interval_t[0]) / 2 - (interval_t[3] - interval_t[2]) / (2 * M)
            z_opt = self.func(x_new)
            newIntervals = ((interval_t[0], x_new, interval_t[2], z_opt), (x_new, interval_t[1], z_opt, interval_t[3]))

            changedM = False
            for interval in newIntervals:
                tmpM = self.r * self.calculateM(interval)
                if tmpM > M:
                    M = tmpM
                    changedM = True

            if changedM or abs(z_opt - z_opt_prev) > 1e-8:
                tmpQ = queue.PriorityQueue()
                while not self.Q.empty():
                    interval = self.Q.get()[1]
                    tmpR = self.calculateR(M, z_opt, interval)
                    tmpQ.put((-tmpR, interval))
                self.Q = tmpQ
            for interval in newIntervals:
                tmpR = self.calculateR(M, z_opt, interval)
                self.Q.put((-tmpR, interval))

            interval_t = self.Q.get()[1]
            z_opt_prev = z_opt
            self.niter += 1
