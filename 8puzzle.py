import sys
from optparse import OptionParser
import math
from struct import pack
import heapq

class Solver:
    def __init__(self, n):
        self.N = n
        self.L = n * n

        self.GOAL = range(1, self.L)
        
        # slide rules
        self.SR = {}
        for i in range(self.L):
            s = []
            if i - self.N >= 0:
                s.append(i - self.N)
            if (i % self.N) - 1 >= 0:
                s.append(i - 1)
            if (i % self.N) + 1 < self.N:
                s.append(i + 1)
            if i + self.N < self.L:
                s.append(i + self.N)
            self.SR[i] = s

        # queue
        self.queue = []
        self.enqueued = {}

        # verbose
        #self.verbose = 104999
        self.verbose = 8963

        # h
        self.w = 1
        self.h = self.heuristics

    def is_solvable(self, tiles):
        x = 0
        for p in range(len(tiles)):
            a = tiles[p]
            if a < 2 :
                continue
            for b in tiles[p:]:
                if b == 0:
                    continue
                if a > b:
                    x = x + 1
        return (x & 1) == 0

    def neighbors(self, tiles):
        n = []
        a = tiles.index(0)
        for b in self.SR[a]:
            n.append(self.swap(list(tiles), a, b))
        return n

    def swap(self, tiles, a, b):
        tiles[a], tiles[b] = tiles[b], tiles[a]
        return tiles

    def display(self, tiles):
        for i in range(self.L):
            if tiles[i]:
                print ('%(n)#2d' % {'n': tiles[i]})
            else:
                print ('  ')
            if i % self.N == self.N - 1:
                print

    def enqueue(self, state):
        (tiles, parent, h, g) = state

        if self.verbose > 0 and len(self.enqueued) % self.verbose == self.verbose - 1:
            print (" -->", len(self.enqueued), g)

        f = h * self.w + g;
        heapq.heappush(self.queue, (f, state))

    def dequeue(self):
        if len(self.queue) <= 0:
            return None
        (f, state) = heapq.heappop(self.queue)
        return state

    def heuristics(self, tiles):
        return 0;

    def manhattan(self, tiles):
        h = 0
        for i in range(self.L):
            n = tiles[i]
            if n == 0:
                continue
            h += int(abs(n - 1 - i) / self.N) + (abs(n - 1 - i) % self.N)
        return h

    def hamming(self, tiles):
        h = 0
        for i in range(self.L):
            n = tiles[i]
            if n > 0 and n - 1 != i:
                h += 1
        return h

    def solve(self, initial):
        if not self.is_solvable(initial):
            return None

        state = (initial, None, self.h(initial), 0);
        if initial == self.GOAL:
            return state

        self.enqueue(state)

        while True:
            state = self.dequeue()
            if (not state):
                break

            (tiles, parent, h, g) = state
            neighbors = self.neighbors(tiles)
            for n_tiles in neighbors:
                if n_tiles == self.GOAL:
                    return (n_tiles, state, 0, g + 1)

                packed = pack(self.L*'B', *n_tiles)
                if (packed in self.enqueued):
                    continue;
                self.enqueued[packed] = True

                n_state = (n_tiles, state, self.h(n_tiles), g + 1)
                self.enqueue(n_state)

def main(options, args):
    initial = []
    if args:
        for n in args:
            initial.append(int(n))
    else:
        initial = [8,7,6,5,4,3,2,1,0]

    solver = Solver(int(math.sqrt(len(initial))))

    solver.verbose = int(options.verbose)
    solver.w = float(options.weight)
    if int(options.function) == 1:
        solver.h = solver.hamming
    elif int(options.function) == 2:
        solver.h = solver.manhattan

    state = solver.solve(initial)
    if not state:
        print ("No solution possible")
        return 1

    solution = []
    while state:
        (tiles, parent, h, g) = state
        solution.insert(0, tiles)
        state = parent

    n = 0
    for tiles in solution:
        print ("#", n)
        solver.display(tiles)
        print
        n += 1

    print ("Number of states enqueued =", len(solver.enqueued))
    return 0

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] [tile] [tile] [tiles ...]")
    parser.add_option("-v", "--verbose", metavar="<level>",
            default=8963)
    parser.add_option("-f", "--function", metavar="<fid>",
            help="heuristics function. 1 for hamming, 2 for manhattan [default: None as breadth first]",
            default=0)
    parser.add_option("-w", "--weight", metavar="<n>",
            help="weighting of the heuristics function [default: 1]",
            default=1)
    (options, args) = parser.parse_args()

    sys.exit(main(options, args))