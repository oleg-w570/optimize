import heapq

from modules.utility.interval import Interval


class TrialDataItem:
    def __init__(self,
                 characteristic: float,
                 interval: Interval):
        self.characteristic: float = characteristic
        self.interval: Interval = interval
        
    def __lt__(self, other) -> bool:
        return self.characteristic > other.characteristic
    
    def __repr__(self) -> str:
        return f'<{self.characteristic}, {self.interval}>'


class TrialData:
    def __init__(self):
        self.queue: list[TrialDataItem] = list()
        
    def insert(self, characteristic: float, interval: Interval):
        heapq.heappush(self.queue, TrialDataItem(characteristic, interval))
        
    def get_intrvl_with_max_r(self) -> Interval:
        return heapq.heappop(self.queue).interval

    def get_n_intrvls_with_max_r(self, n: int) -> list[Interval]:
        intervals = []
        for _ in range(n):
            intervals.append(heapq.heappop(self.queue).interval)
        return intervals
    
    def refill(self):
        heapq.heapify(self.queue)
        
    def size(self) -> int:
        return len(self.queue)
    
    def __iter__(self):
        return iter(self.queue)
