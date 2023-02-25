import random
from itertools import product
from threading import Thread
from timeit import default_timer as timer
import queue

DIGITS = set(range(1, 10))

def duplicate_checker(a):
        b = set(a)
        result = len(a) != len(b)
        #print(result)
        if(result == True):
            return True

#---------------------------------------------------------------------------------------------------------------
# 3 x 3

def display_grid3(grid):
    print("")
    count =1
    print("   1  2  3")
    for x in grid:
        
        print(count,x,end=" ")
        count+=1
        print()
        
def scramble3(grid):
    for x in range(6):
        y = random.randint(0,2)
        x = random.randint(0,2)
        grid[x][y] = 0

def check_grid_size3(grid):
    """Check that the grid is 3x3."""
    well_formed = len(grid) == 3 and all(len(row) == 3 for row in grid)
    return well_formed or None


def check_rows3(grid, q):
    """Check that each number appears exactly once per row."""
    q.put(all(set(row) == DIGITS for row in grid))


def check_columns3(grid, q):
    """Check that each number appears exactly once per column."""
    columns = [[row[c] for row in grid] for c in range(3)]
    q.put(all(set(col) == DIGITS for col in columns))





def check_sudoku3(grid):
    """
    Validate a sudoku solution.

    Given a grid as a list of lists, return None if it is ill-formed,
    False if it is invalid, or True if it is a valid solution.
    """

    """The isinstance() function returns True if the specified object is of the specified type, otherwise False
    """
    assert isinstance(grid, list)

    q = queue.Queue()

    if not check_grid_size3(grid):
        return None

    """Thread in python takes to arguements , target hwere the target function is put with which parallel processing has to be done
    and the arguments which the function takes"""

    row_thread = Thread(target=check_rows3, args=(grid, q))
    row_thread.start()

    columns_thread = Thread(target=check_columns3, args=(grid, q))
    columns_thread.start()

    grid_threads = []

    """The string join() method returns a string by joining all the elements of 
    an iterable (list, string, tuple), separated by the given separator."""
    row_thread.join()
    columns_thread.join()

    [t.join() for t in grid_threads]

    results = []
    while not q.empty():
        results.append(q.get())

    return all(results)
        


#-----------------------------------------------------------------------------------------------------------------
#9 x 9

def check_grid_size(grid):
    """Check that the grid is 9x9."""
    """checks the length of grid and traverses through each row """
    """all() function returns True if all items in an iterable are true"""
    well_formed = len(grid) == 9  and all(len(row) == 9 for row in grid)
    return well_formed or None


def check_rows(grid, q):
    """Check that each number appears exactly once per row."""
    """This method is used to add an element in the queue which can be represented as an instance of Queue"""
    """all() function returns True if all items in an iterable are true"""
    q.put(all(set(row) == DIGITS for row in grid))


def check_columns(grid, q):
    """Check that each number appears exactly once per column."""
    """The set() function creates a set object. The items in a set list are unordered, so it will appear in random order."""
    columns = [[row[c] for row in grid] for c in range(9)]
    q.put(all(set(col) == DIGITS for col in columns))


def check_3x3_grid(grid, q):
    """Check that each number appears exactly once per 3x3 grid."""
    threes = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    for row_block, col_block in product(threes, threes):
        block = [grid[r][c] for r, c in product(row_block, col_block)]
        if set(block) != DIGITS:
            q.put(False)
            return

    q.put(True)


def check_sudoku(grid):
    """
    Validate a sudoku solution.

    Given a grid as a list of lists, return None if it is ill-formed,
    False if it is invalid, or True if it is a valid solution.
    """
    """The assert keyword lets you test if a condition in your code returns True, 
    if not, the program will raise an AssertionError."""

    assert isinstance(grid, list)

    q = queue.Queue()

    if not check_grid_size(grid):
        return None

    row_thread = Thread(target=check_rows, args=(grid, q))
    row_thread.start()

    columns_thread = Thread(target=check_columns, args=(grid, q))
    columns_thread.start()

    grid_threads = []
    for _ in range(9):
        t = Thread(target=check_3x3_grid, args=(grid, q))
        t.start()
        grid_threads.append(t)

    row_thread.join()
    columns_thread.join()

    [t.join() for t in grid_threads]

    results = []
    while not q.empty():
        results.append(q.get())

    return all(results)



def display_grid(grid):
    print("")
    print("")
    print("         Martin's Sudoku")
    print("")
    count =0
    print("      1 2 3   4 5 6   7 8 9")
    print("   ---------------------------")
    for x in grid:
        print(count+1,end="   ")
        for y in range(len(x)):
            if(y % 3 != 0):
                print(x[y],end=" ")
            else:
                print("|",x[y],end=" ")
        print("|",end=" ")
        count+=1
        print()
        if(count % 3 == 0):
            print("   ---------------------------")
def rearrange(a):
    temp=[[],[],[],[],[],[],[],[],[]]
    count =0
    ch = 0
    for e in range(len(a)):
        for x in range(3):
            if(a[e][x]!=0):
                temp[ch].append(a[e][x])
        count+=1
        if(count ==3):
            ch+=1
            count = 0
    for e in range(len(a)):
        for x in range(3,6):
            if(a[e][x]!=0):
                temp[ch].append(a[e][x])
        count+=1
        if(count ==3):
            ch+=1
            count = 0
    for e in range(len(a)):
        for x in range(6,9):
            if(a[e][x]!=0):
                temp[ch].append(a[e][x])
        count+=1
        if(count ==3):
            ch+=1
            count = 0
    return temp       
def scramble():
    global grid
    amount = 40
  
    for i in range(amount):
        y = random.randint(0,len(grid)-1)
        x = random.randint(0,len(grid)-1)
        num = random.randint(1,len(grid))
        allow = 0
        for e in range(len(grid)):
            if num not in grid[x] and num != grid[e][y]:
                allow +=1
        grid[x][y] = num
        tempo = grid     
        tempo = rearrange(tempo)
        
        for e in range(len(grid)):
            if(duplicate_checker(tempo[e])):
                allow = 0
        if allow !=len(grid):
            grid[x][y] = 0
               
#------------------------------------------------------------------------------------------------------------------------------------
#MAIN CALLING


print("WELCOME TO THE GAME OF SUDOKU")
print("PLEASE CHOOSE WHICH SUDOKU WOULD YOU LIKE TO PLAY ->")
print("1) 3 X 3")
print("2) 9 x 9")   

choice1=int(input("Enter your choice"))  


if choice1==1:

    grid = [[1, 2, 3],[3, 1, 2] ,[2, 3, 1]]

    solved = False
    scramble3(grid)
    display_grid3(grid)

    while solved != True:
        y = int(input(" enter row "))-1
        x = int(input("enter column "))-1
        num = int(input("enter number]"))
        
        if grid[y][x] == 0:
            grid[y][x] = num
        else:
            if input("overwrite? [y/n]") == "y":
                grid[y][x] = num
            
        display_grid3(grid)

        full = True
        for x in grid:
            for y in x:
                if(y == 0):
                    full = False
    
        if(full ==True):
            if(check_sudoku3(grid)==False):
                print("The solution is incorrect")
            else:
                print("solved")
                solved =True



if choice1==2:

    grid = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

    solved = False
    scramble()
    display_grid(grid)


    while solved != True:
        x = int(input("enter horizontal [1,9]"))-1
        y = int(input("enter vertical [1,9] "))-1
        
        num = int(input("enter number"))
        
        if grid[y][x] == 0:
            grid[y][x] = num
        else:
            if input("overwrite? [y/n]") == "y":
                grid[y][x] = num
            
        display_grid(grid)
        full = True
        for x in grid:
            for y in x:
                if(y == 0):
                    full = False
        if(full ==True):
            if(check_sudoku(grid)==False):
                print("The solution is incorrect")
            else:
                print("solved")
                solved =True
        