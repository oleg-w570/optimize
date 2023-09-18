import heapq

from modules.utility.intervaldata import IntervalData


class TrialDataItem:
    def __init__(self,
                 characteristic: float,
                 interval: IntervalData):
        self.characteristic: float = characteristic
        self.interval: IntervalData = interval
        
    def __lt__(self, other) -> bool:
        return self.characteristic > other.characteristic
    
    def __repr__(self) -> str:
        return f'<{self.characteristic}, {self.interval}>'


class TrialData:
    def __init__(self):
        self.intrvl_queue: list[TrialDataItem] = list()
        
    def insert(self, characteristic: float, interval: IntervalData):
        heapq.heappush(self.intrvl_queue, TrialDataItem(characteristic, interval))
        
    def get_intrvl_with_max_r(self) -> IntervalData:
        return heapq.heappop(self.intrvl_queue).interval
    
    def refill(self):
        heapq.heapify(self.intrvl_queue)
    
    def __iter__(self):
        return iter(self.intrvl_queue)
