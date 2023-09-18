
from modules.utility.intervaldata import IntervalData
from modules.core.trial_data import TrialData
from modules.utility.point import Point
# 
# a = [(1, 'a'), (3, 'b'), (5, 'c'), (2, 'd'), (4, 'e')]
# print(f'Source -> {a}')
# 
# heapq.heapify(a)
# print(f'After heapify -> {a}')
# 
# smallest = heapq.nsmallest(3, a)
# print(f'First 3 smallest -> {smallest}')
# print(f'After getting smallest -> {a}')

a = TrialData()
a.insert(10, IntervalData(Point(1, [1], 1)))
a.insert(12, IntervalData(Point(1, [1], 1)))
a.insert(11, IntervalData(Point(1, [1], 1)))
a.insert(15, IntervalData(Point(1, [1], 1)))

for item in a:
    print(item)
