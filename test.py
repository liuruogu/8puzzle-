import random

goal = [[1,2,3],
        [4,5,6],
        [7,8,0]]

def fGoal(goal, value):
# find the value and return the row, col coordinates

        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if goal[row][col] == value:
                    return row, col

def index(item, seq):
# return index of the sequence. Return -1 if can not find the index
    if item in seq:
        return seq.index(item)
    else:
        return -1


class EightPuzzle:

    def __init__(self):
# heuristic value
        self.heurVal = 0
# search depth of current instance
        self.depth = 0
# The specified node
        self.adj_matrix = []
# insert the goal state for as the
        for i in range(3):
            self.adj_matrix.append(goal[i][:])

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res


    def _clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def _get_legal_moves(self):
        # get row and col of the empay space
        row, col = self.find(0)
        free = []

        # find which pieces can move there
        if row > 0:
            free.append((row - 1, col)) #up
        if col > 0:
            free.append((row, col - 1)) #left
        if row < 2:
            free.append((row + 1, col)) #down
        if col < 2:
            free.append((row, col + 1)) #right

        return free

    def _generate_moves(self):
        #Get the cooradinate of lebal move
        free = self._get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a, b)
            p.depth = self.depth + 1
            p.parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)


#check if the 8-puzzle can be solve
    def _isValid(self):
        return 1

#set a new puzzle by user
    def set(self, other):
        i = 0;
        for row in range(3):
            for col in range(3):
                self.adj_matrix[row][col] = int(other[i])
                i=i+1

    def solve(self, h):

#if adjacent equals to goal state, then this problem is solved
        def is_solved(puzzle):
            return puzzle.adj_matrix == goal
        #The initial node into the queue
        frontier = [self]
        #The visited node List
        closedl = []
        #The nodes I expanded
        move_count = 0
        #The queue Count
        max_queue = 0
        #The length of queue
        len_queue = 0
        while len(frontier) > 0:

            x = frontier.pop(0)
            #The node I have explored
            print("The", move_count+1, "node we explored")
            print(x, end="")
            x.heurVal = h(x)
            print("g(x)=", x.depth, "h(x)=", x.heurVal)
            print()
            move_count += 1
            if (is_solved(x)):
                print("The depth of the goal node is", x.depth)
                print("The maximun number of the node in the queue is", max_queue)
                if len(closedl) > 0:
            #Return the soultion path and move count
                    return  move_count
                else:
                    return [x]

            succ = x._generate_moves()
            for move in succ:
                # have we already seen this node?
                idx_open = index(move, frontier)
                idx_closed = index(move, closedl)
                #calculate the heuristic of each move
                hval = h(move)
                fval = hval + move.depth

                if idx_closed == -1 and idx_open == -1:
                    move.heurVal = hval
                    frontier.append(move)
                elif idx_open > -1:
                    copy = frontier[idx_open]
                    if fval < copy.heurVal + copy.depth:
                        # copy move's values over existing
                        copy.heurVal = hval
                        copy.parent = move.parent
                        copy.depth = move.depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy.heurVal + copy.depth:
                        move.heurVal = hval
                        closedl.remove(copy)
                        frontier.append(move)

            closedl.append(x)

            #priortize the node in priority queue based on the heuristic + depth
            frontier = sorted(frontier, key=lambda p: p.heurVal + p.depth)
            #Get the maximum number of nodes in the queue at any one time
            len_queue = len(frontier)
            if max_queue <= len_queue:
                max_queue = len_queue

        return [], 0

    def shuffle(self, step_count):
        for i in range(step_count):
            row, col = self.find(0)
            free = self._get_legal_moves()
            target = random.choice(free)
            self.swap((row, col), target)
            row, col = target

    def find(self, value):
# find the value and return the row, col coordinates
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def adj(self, row, col):
#Return the value of the specified row and col
        return self.adj_matrix[row][col]

    def poke(self, row, col, value):
        self.adj_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        temp = self.adj(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.adj(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)

#uniform cost search
def h_default(puzzle):
    return 0

# Misplaced heuristic
def h_misplaced(puzzle):
    m = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.adj(row, col)
            if(val!= goal[row][col]):
                m+=1
    return m

# Manhattan heuristic
def h_manhattan(puzzle):
    t = 0
    for row in range(3):
        for col in range(3):
            r_val = row
            c_val = col
            val = puzzle.adj(row, col)
            target_row, target_col = fGoal(goal, val)
            t += abs(r_val - target_row)+abs(c_val-target_col)
    return  t

def main():

    p = EightPuzzle()

    print("Welcome to Ruogu Liu's 8-puzzle solver")
    pz =  input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle ")
    if  pz == "1":
#       default puzzle set by yourself
        p.set("123480765")


    elif pz == "2":
        print("Your choice is ", pz + ", Please input your own puzzle")
        SetPuzzle = input()
        p.set(SetPuzzle)

    print("Enter your choice of algorithm")
    print("1. Uniform Cost Search")
    print("2. A* with the Misplaced Tile heuristic")
    print("3. A* with the Manhattan distance heuristic")

    choice = input()

    if choice == "1":
         count = p.solve(h_default)
         print ("Solved!!!  with uniformed cost search by exploring", count, "nodes")


    elif choice == "2":
         count = p.solve(h_misplaced)
         print ("Solved!!! with misplaced distance by exploring", count, "nodes")

    elif choice =="3":
         count = p.solve(h_manhattan)
         print ("Solved!!! with Manhattan distance by exploring", count, "nodes")

if __name__ == "__main__":
    main()