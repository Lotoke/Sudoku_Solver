# Sudoku Solver

The aim of this project was to create a program that takes a 3D numpy array representation of a sudoku puzzle and return either the correct solution or an array of -1's in the same format.

The program uses a depth first search algorithm to explore the possible states that the sudoku can take for each valid number that can go into a blank cell.

## Optimisations:

A basic depth first search algorithm has exponential time complexity and the recursive approach uses large amounts of memory, therefore backtracking needed to be minimised.
The main optimisation applied was constraint satisfaction. This was implemented by giving each empty cell of the sudoku a 'domain' of possible values it can take within the constraints (rules) of the puzzle. Every time one of the empty cells is filled in, all of the domains are updated. This significantly reduces the number of paths that need to be explored to find a solution, and helps to identify paths than will not lead to the goal.

A further optimization was made by ordering the empty cells by the number of values in their domains, and choosing the cells with less domain values to be explored first. For example, filling all of the spaces that only have one possible value first narrows down the remaining domains. The very easy to medium sodukus solve very quickly as the cell with the smallest domain is picked each time and no backtracking is required.

## Functions and Classes:

### Cell:

The cell class contains the position and domain of empty space in the sudoku. Using an object to hold these values makes it easier to keep track of the position associated with each domain.

### SudokuState:

The sudoku_state class holds a numpy representation of the sudoku and provides methods that operate on it.

- get_domains():

  - The domains are found by identifying the position of all zeros (empty cells) in the sudoku, and creating a list combining the values from the column, row and 3x3 quadrant that each zero corresponds to. The domain is calculated from this combined list by removing the repeated values.
    For each 0, a cell object is created containing its position and associated domain. The cell objects are stored in the list attribute 'domains'.

- order():

  - Orders the list of cell objects in ascending order by the length of their 'domain' attribute.

- is_valid() and is_valid_domain():
  - The difference between these two methods is that 'is_valid' iterates through the entire sudoku state and checks that there are no missing or repeated values (which would make the state invalid), while 'is_valid_domains' simply makes sure that each empty cell can still be filled with a correct value. 'is_valid' is false until the goal state is found, while 'is_valid_domains' will be true until an entire branch has been explored without finding a solution and backtracking is required.

### DFS:

The DFS function is an adapted version of the depth first search function from an eight queens puzzle solver. DFS performs depth first search on many possible moves that can be made. The result of each move is a 'partial state', which acts as a node in a search tree.  
This function is initiated with a partial sudoku state (numpy array), and the domains and positions of each empty cell are calculated and stored in the 'domain' list.

Example 'domain list' of empty cells:  
`domain = [cell[[x,y], [domain]], cell[[0,0],[1]], cell[[5,1],[7,3]], cell[[6,4],[9,4,1,8]]`

The DFS process is outlined below:

**For a given partial state:**

- Program starts with the cell that has the least number of options for possible values (shortest domain length).

- The first blank cell is filled in with the first value of its domain.

- All domains are recalculated and checked if they are valid (they are only valid if all empty cells still have values they can be filled with).

  - If they are valid, the DFS function is called recursively on the new partial state and the program progresses deeper into search tree. The new 'child' state passed into the DFS function is a deep copy of the parent.

  - If any of the domains are invalid, the current path will not lead to a correct solution so program will backtrack to the previous partial state.

  - If the partial state is the goal state, all recursive instances are popped off the call stack and the solved sudoku is returned.

When the program backtracks, it returns to the parent of the sudoku state it came from and chooses the next number in the current cell's domain. If it iterates through all domain values without finding a suitable suitable value for that cell, the program backtracks further.

## Evaluation & Improvements:

The agent is able to solve all provided sudokus correctly within a 'reasonable' amount of time. On the hardware the code was tested with, medium sudokus often solved in less than 0.01 seconds. Hard sudokus that had valid solutions could be solved in less than 4 seconds however it took over 8 seconds to determine if a hard sudoku was invalid. As previously mentioned, reducing the number of times backtracking is required could significantly improve the time complexity. Ordering the cells by length of their domains significantly reduced the solve time for hard sudokus, however the values picked from the domains to fill cells is largely trial and error.  
As described by Kevin Coulombe (Coulombe, 2010), it is sometimes possible to deduce which value must go in in a specific cell by looking at the other empty cells in the same quadrant, column and row. For example, if one of the domain values of an empty cell is 4, and the domains of all other cells in the same quadrant do not contain a 4, then the correct value for this cell must be 4. Further improvements may be possible by investigating strategies humans use to complete sudokus.

## References:

- Eight Queens Solver: https://moodle.bath.ac.uk/course/view.php?id=59592&section=6

- Coulombe, K., 2010. Sudoku solver - Byte Author. [online] Byteauthor.com. Available from: http://byteauthor.com/2010/08/sudoku-solver/ [Accessed 10 Mar. 2021].
