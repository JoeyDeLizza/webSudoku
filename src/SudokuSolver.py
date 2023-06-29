from queue import PriorityQueue
import sys

## Holds Sudoku board data and provides functions for iteratoring over indexes
class Sudoku:

    ## Initializes gamedata with either a file or a string of gamedata
    def __init__(self, file):
        if type(file) == type(''):
            self.gamedata = file
        else:
            self.gamedata = file.read()
        self.gamedata = self.gamedata.translate({ord(i): None for i in ' \n'}) 
        self.size = 9

    ## Returns a function to iterate over values in the same row as i
    def rowIter(self, i):
        row = i // self.size
        return lambda j : self.__rowIter__(row, j)
    
 
    ## Returns a function to iterate over values in the same col as i
    def colIter(self, i):
        col = i % (self.size)
        return lambda j : self.__colIter__(col, j)

    ## Returns a function to iterate over values in the same cell as i
    def cellIter(self, i):
        col = i % (self.size)
        row = i // self.size
        cell = 3 * self.__cellRow__(row) + self.__cellCol__(col)

        return lambda j : self.__cellIter__(row, col, cell, j)
    
    def solved(self):
        row = '123456789'
        col = '123456789'
        cell = '123456789'

        row_indexes = [0, 9, 18, 27, 36, 45, 54, 63, 72]
        col_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        cell_indexes = [0, 3, 6, 27, 30, 33, 45, 48, 51]

        for r in row_indexes:
            rowIter = self.rowIter(r)
            row = '123456789'

            for i in range(0, 9):
                row = row.replace(self.gamedata[rowIter(i)], '')
            if row != '':
                return False

        for c in col_indexes:
            colIter = self.colIter(c)
            col = '123456789'

            for i in range(0, 9):
                col = col.replace(self.gamedata[colIter(i)], '')
            if col != '':
                return False

        for ce in cell_indexes:
            cellIter = self.cellIter(ce)
            cell = '123456789'

            for i in range(0, 9):
                cell = cell.replace(self.gamedata[cellIter(i)], '')
            if cell != '':
                return False


        return True
        
        return True
    def __cellIter__(self, row, col, cell, i):
        cellRow = self.__cellRow__(row)
        if cellRow == 0:
            start_i = 0
        elif cellRow == 1:
            start_i = 27
        elif cellRow == 2:
            start_i = 54
        return (((i // 3) * 9 + (i % 3) ) + start_i) + (3 * self.__cellCol__(col))
    
    def __cellCol__(self, col):
        return col // 3

    def __cellRow__(self, row):
        
       return row // 3
   
    def __colIter__(self, col, i):
        return (i * self.size) + col

    def __rowIter__(self, row, i):
        last = (row + 1) * self.size - 1
        if i >= self.size:
            i = row * self.size
        return i + (row * self.size)

    
    def __repr__(self):
        s = ''
        for i in range(0, len(self.gamedata)):
            s += self.gamedata[i] + ' '
            if (i + 1) % self.size == 0:
                s += '\n'
        return s

## Object for solving Sudoku Objects
class SudokuSolver:

    ## Initializes Variables, Domains, Constraints, Availability list
    def __init__(self, s):
        self.sod = s
        self.X = self.sod.gamedata
        self.D = self.__initDomain__()
        self.C = self.__initCons__()
        self.A = self.__initAvailList__()
        self.solved = False
        if not self.A:
            return None
        


    
        
        
        
    def solvable(self, S):
        sol = SudokuSolver(S)
        return sol.A

    ## prints solution
    def solve(self):
        S = self.__search__(self.X)
        if S.solved():
            return S
        else:
            return None

    ## Returns goal state as a Sudoku object
    def __search__(self, X):
        i = len(self.A)-1
        node = self.A[i]
        found = False
        q = self.__initPQ__()
        node = q.get()
        self.fastExpand(node, q)
        return Sudoku(self.X)
        
        
    def setString_i(self, i, s, c):
        return s[:i] + c + s[i + 1:]

    ## searches for goal state using most constraining variable as heuristic
    def fastExpand(self, node, q):
        node = q.get()
        cons = node[1]
        i = cons[0]

        sol = SudokuSolver(Sudoku(self.X))
        if q.empty() or self.solved:
            self.X = self.setString_i(i, self.X, cons[1])
            self.solved = True
            return

        for j in cons[1]:
            newX = self.setString_i(i , sol.X, j)
            sol = SudokuSolver(Sudoku(newX))

            if sol.A:
                newNode = q.get()
                sol.fastExpand(newNode, sol.__initPQ__())
                if sol.solved:
                    self.solved = True
                    self.X = sol.X
                    return
            
        
    ## recursively searches for goal state
    def expand(self, node, i, found):
        sol = SudokuSolver(Sudoku(self.X))
        if i == -1 or self.solved:
            self.solved = True
            p = self.X
            return 
        for j in node:
            newX = self.setString_i(i, sol.X, j)
            sol = SudokuSolver(Sudoku(newX))
            if sol.A:
                newNode = sol.A[i-1]
                sol.expand(newNode, i-1, found)
                if sol.solved:
                    self.solved = True
                    self.X = sol.X
                    return 
            
            
            
    def test(self, l):
        l.pop()
        print(l)
      
    def printQ(self, q):
        count = 0
        while not q.empty():
            i = q.get()
            count = count + 1
            print(i)
        print(count)

    def __initPQ__(self):
        queue = PriorityQueue()
        index = 0
        for i in self.A:
            if i == self.X[index]:
                index = index + 1
                continue
            else:
                if len(i):
                    queue.put((len(i), (index, i) ))
            index = index + 1
        return queue
        
    def __initDomain__(self):
        D = []
        values = '123456789'
        for i in self.X:
            if i != '0':
                D.append(i)
            else:
                D.append(values)
        return D

    def __initAvailList__(self):
        A = []
        index = 0
        for cons in self.C:
            avail = self.D[index]
            if self.X[index] != '0':
                avail = avail 
            else:
                for char in cons:
                    avail = avail.replace(char, '')
            index = index + 1
            if avail == '':
                return False
            A.append(avail)
        
        return A
    
    def __initCons__(self):
        cons = []
        index = 0
        for d in self.D:
            d_cons = ''
            d_cons = d_cons + self.__rowCons__(index)
            d_cons = d_cons + self.__colCons__(index)
            d_cons = d_cons + self.__cellCons__(index)
            d_cons = ''.join(set(d_cons))
            if d == None:
                d_cons = None
            cons.append(d_cons)
            index = index + 1
        return cons

    def __rowCons__(self, i):
        iter = self.sod.rowIter(i)
        return self.__grabCons__(iter)

    def __colCons__(self, i):
        iter = self.sod.colIter(i)
        return self.__grabCons__(iter)

    def __cellCons__(self, i):
        iter = self.sod.cellIter(i)
        return self.__grabCons__(iter)

    def __grabCons__(self, iter):
        cons = ''
        for i in range(0, 9):
            c = iter(i)
            if self.sod.gamedata[c] in cons or self.sod.gamedata[c] == '0':
                continue
            else:
                cons = cons + self.sod.gamedata[c]
        return cons
x = Sudoku(sys.argv[1])
s = SudokuSolver(x)
result = s.solve()
if result == None:
    empty = "0" * 81
    print(empty)
else:
    print(result.gamedata)
sys.stdout.flush()

