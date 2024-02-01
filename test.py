import numpy as np
import copy
class Cell: #Object contains domain and coordinates of specific blank space 
    def __init__(self, domain=[], pos=[]):
        self.domain=domain
        self.pos=pos
    def __repr__(self):
        return str([self.domain, self.pos])

class SudokuState:#
    def __init__(self, puzzle):
        self.n = None
        self.state=puzzle# 3D Array representation of sudoku puzzle
        self.vars = [] #
        self.quadrant=[] 
        self.row=[]
        self.column=[]
        self.domains=[]

    def getDomain(self):
        #resets attributes
        self.domains=[]
        self.vars=[]
        self.row=[]
        self.column=[]
        self.quadrant=[]
        x=0
        y=0
        self.vars.append(np.where(self.state==0)) #Finds position of all 0s 
        yVars=self.vars[0][0] #array of y positions of 0s
        xVars=self.vars[0][1] #array of x positions of 0s
        

        for n in range(0, len(yVars)):
            y= yVars[n]
            x= xVars[n]
            self.row.append(self.state[y,:].tolist()) #get rows of sudoku where 0s occur
            self.column.append(self.state[:, x].tolist()) #get columns of sudoku where 0s occur
            #gets all 3x3 quadrants where 0s occur and stores as an array of arrays.
            self.quadrant.append(self.state[(y//3)*3, (x//3)*3:(x//3)*3+3].tolist()+self.state[(y//3)*3+1, (x//3)*3:(x//3)*3+3].tolist()+self.state[(y//3)*3+2, (x//3)*3:(x//3)*3+3].tolist())

            presentVals=list(dict.fromkeys(self.row[n]+ self.column[n]+self.quadrant[n]))
            tempDomain=[]
            for i in range (0,10):
                if i not in presentVals:
                    tempDomain.append(i) #array with redundant values removed (domain)
            #creates cell object containing position of 0 and associated domain
            #all cells stored in 'domains' array 
            self.domains.append(Cell(tempDomain,[xVars[n],yVars[n]])) 

        return self.order() #returns array of domains ordered by length
    def order(self):
        #orders array in ascending order by length of the domain attribute of each cell
        self.domains= sorted(self.domains, key=lambda cell: len(cell.domain)) 
        return self.domains

    def isValid(self):
        #reset attributes
        self.row=[]
        self.column=[]
        self.quadrant=[]

        for y in range(0,9,3):
            for x in range(0,9,3):
                #array containing all 3x3 quadrants of sudoku
                self.quadrant.append(self.state[y,x:x+3].tolist()+self.state[y+1,x:x+3].tolist()+self.state[y+2,x:x+3].tolist())        
        for n in range (1,10):
            for i in range(0,8):
                #array containing all rows of sudoku
                self.row.append(self.state[i,:].tolist()) 
                #array containing all columns of sudoku
                self.column.append(self.state[:, i].tolist())

                #checks for repeated numbers in each row column and quadrant 
                # state is invalid if this is the case
                if n not in self.row[i] or n not in self.column[i] or n not in self.quadrant[i]: 
                    return False
        return True
    def isValidDomains(self):
        #if a domain contains [], there are no possible solutions for the state
        return not any(cell.domain == [] for cell in self.domains) 
      
    def isGoal(self):
        #goal state found if domains array is empty
        if len(self.domains) == 0: 
            return True
        else:
            return False
    def set_var(self, xPos, yPos, val):
        #sets changes value of sudoku at position (xPos,yPos) to val
        self.state[yPos, xPos]= val 
    def copy(self):
        return copy.copy(self.state) #deep copy of sudoku state


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    def DFS (partial):
        partialState = SudokuState(partial) #create sudoku state
        domain = partialState.getDomain() #get domains of sudoku
 

        for cell in domain: #iterate cell objects in domain

            #iterate through domain attribute of each cell- domain of each 0 
            for n in range(0, len(cell.domain)):
                #set current position of 0 to nth value of corresponding domain
                partialState.set_var(cell.pos[0], cell.pos[1], cell.domain[n]) 
                domain=partialState.getDomain()

                if partialState.isValid() and partialState.isGoal(): 
                    #return if partial state is now the valid goal state
                    return partialState
                if partialState.isValidDomains():
                    #search child of partialState
                    searchState=DFS(partialState.copy())

                    if searchState is not None and searchState.isValid() and searchState.isGoal():
                        #if invalid state reached backtrack to last valid state
                        return searchState
             
            return None
    sol= DFS(sudoku)
    if sol == None:
        return np.full((9,9), -1) #sudoku can't be solved
    else:
        return sol.state #solution
    
    return solved_sudoku