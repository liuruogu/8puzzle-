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
        self._hval = 0
        # search depth of current instance
        self._depth = 0
        # parent node in search path
        self._parent = None
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
        # get row and column of the empty piece
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
            p._depth = self._depth + 1
            p._parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def _generate_solution_path(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent._generate_solution_path(path)
    def set(self, other):
        i = 0;
        for row in range(3):
            for col in range(3):
                self.adj_matrix[row][col] = int(other[i])
                i=i+1


    def solve(self, h):
        """Performs A* search for goal state.
        h(puzzle) - heuristic function, returns an integer
        """
        def is_solved(puzzle):
            return puzzle.adj_matrix == _goal_state

        openl = [self]
        closedl = []
        move_count = 0
        while len(openl) > 0:
            x = openl.pop(0)
            move_count += 1
            if (is_solved(x)):
                if len(closedl) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            succ = x._generate_moves()
            idx_open = idx_closed = -1
            for move in succ:
                # have we already seen this node?
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move._depth

                if idx_closed == -1 and idx_open == -1:
                    move._hval = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy._hval + copy._depth:
                        # copy move's values over existing
                        copy._hval = hval
                        copy._parent = move._parent
                        copy._depth = move._depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy._hval + copy._depth:
                        move._hval = hval
                        closedl.remove(copy)
                        openl.append(move)

            closedl.append(x)
            openl = sorted(openl, key=lambda p: p._hval + p._depth)

        # if finished state not found, return failure
        return [], 0

    def find(self, value):
        """returns the row, col coordinates of the specified value
           in the graph"""
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def peek(self, row, col):
        """returns the value at the specified row and column"""
        return self.adj_matrix[row][col]

    def poke(self, row, col, value):
        """sets the value at the specified row and column"""
        self.adj_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        """swaps values at the specified coordinates"""
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)


def heur(puzzle, item_total_calc, total_calc):
    """
    Heuristic template that provides the current and target position for each number and the
    total function.

    Parameters:
    puzzle - the puzzle
    item_total_calc - takes 4 parameters: current row, target row, current col, target col.
    Returns int.
    total_calc - takes 1 parameter, the sum of item_total_calc over all entries, and returns int.
    This is the value of the heuristic function
    """
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.peek(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            # account for 0 as blank
            if target_row < 0:
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)

#some heuristic functions, the best being the standard manhattan distance in this case, as it comes
#closest to maximizing the estimated distance while still being admissible.



def heur_default(puzzle):
    return 1

def h_misplaced(puzzle):
    return 1

def h_manhattan(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

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
         print ("Solved with Manhattan distance exploring", count, "states")

    print (p)

    path, count = p.solve(h_manhattan)
    # path.reverse()
    for i in path:
        print (i)


if __name__ == "__main__":
    main()