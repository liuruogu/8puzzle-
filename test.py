_goal_state = [[1,2,3],
               [4,5,6],
               [7,8,0]]

def index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
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
        # parent node in search path
        self.parent = None
        self.adj_matrix = []
        for i in range(3):
            self.adj_matrix.append(_goal_state[i][:])

    def __eq__(self, other):
            if self.__class__ != other.__class__:
                return False
            else:
                return self.adj_matrix == other.adj_matrix


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

    def _get_legal_moves(self):
        """Returns list of tuples with which the free space may
        be swapped"""
        # get row and col of the empay space
        row, col = self.find(0)
        free = []

        # find which pieces can move there
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    def _generate_moves(self):
        free = self._get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a, b)
            p.depth = self.depth + 1
            p.parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def _generate_solution_path(self, path):
        if self.parent == None:
            return path
        else:
            path.append(self)
            return self.parent._generate_solution_path(path)

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
#h is the heuristic
    def solve(self, h):
#使用优先队列，并且解释原理。如何保持puzzle的状态。如何比较而且如何找最小的
#if adjacent equals to goal state, then this problem is solved
        def is_solved(puzzle):
            return puzzle.adj_matrix == _goal_state
        #The initial node into the list
        openl = [self]
        #The visited node List
        closedl = []
        move_count = 0
        while len(openl) > 0:
            x = openl.pop(0)
            #The node I have explored
            print("The", move_count+1, "node we explored")
            print(x, end="")
            move_count += 1

            if (is_solved(x)):
                if len(closedl) > 0:
            #Return the soultion path and move count
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            succ = x._generate_moves()

            for move in succ:
                # have we already seen this node?
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move.depth

                if idx_closed == -1 and idx_open == -1:
                    move.heurVal = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
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
                        openl.append(move)
            print("g(x)=", move.depth, "h(x)=", move.heurVal)
            print()
            closedl.append(x)
            openl = sorted(openl, key=lambda p: p.heurVal + p.depth)

        # if finished state not found, return failure
        return [], 0

    def find(self, value):
# find the value and return the row, col coordinates

        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def adj(self, row, col):
#return the value of the adjacent puzzle' value
        return self.adj_matrix[row][col]

    def goal(self, row, col):
        return self.adj_matrix

    def poke(self, row, col, value):
        """sets the value at the specified row and column"""
        self.adj_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        """swaps values at the specified coordinates"""
        temp = self.adj(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.adj(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)


def heur_default(puzzle):
    return 0

def h_misplaced(puzzle):
    return 1


#解释曼哈顿公式的原理
def h_manhattan(puzzle):
    t = 0
    for row in range(3):
        for col in range(3):
            r_val = row
            c_val = col
            val = puzzle.adj(row, col) - 1
            target_col = val % 3
            target_row = val / 3
            if target_row < 0:
                target_row = 2
            t += abs(r_val - target_row)+abs(c_val-target_col)
    return t


def main():

    p = EightPuzzle()

    print("Welcome to Ruogu Liu's 8-puzzle solver")
    pz =  input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle ")
    if  pz == "1":
# default puzzle set by yourself
        p.set("103425786")

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
         path, count = p.solve(heur_default)
         print ("Solved with BFS-equivalent in", count, "moves")

    elif choice == "2":
         path, count = p.solve(h_misplaced)

    elif choice =="3":
         path, count = p.solve(h_manhattan)
         print ("Solved with Manhattan distance exploring", count, "nodes")

if __name__ == "__main__":
    main()