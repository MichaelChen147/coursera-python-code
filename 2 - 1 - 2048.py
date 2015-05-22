"""
Clone of 2048 game.
"""

import poc_2048_gui     
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 


def merge(line):
    """
    Helper function that merges a single row or column in 2048 
    """
    # Iterate through the list and append the list with all
    # non zero values
    newlist = []
    for value in line:
        if value != 0:
            newlist.append(value)  
    newnewlist = []
    holder = 0
    checker = False
    # Iterate through the NEW list. This time keeping track
    #of a holder value, to compare with the next value
    #the various conditions ensure the end product is
    #a complete.
    for value in newlist:
        if (value != 0) and checker == False:
            holder = value
            checker = True
        elif (value != 0) and checker == True and value == holder:
            newnewlist.append(value + holder)
            checker = False
        elif value != 0 and checker == True and value != holder:
              newnewlist.append(holder)
              holder = value

    # This final block of code fills the remainder of 
    # newnewlist with zeroes
    if checker == True:
        newnewlist.append(holder)
    while len(newnewlist) < len(line):
        newnewlist.append(0)
    return newnewlist

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # __init__ first establishes some useful values
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.grid = []
        self.reset()
        # Calculate the row/column for each direction
        upindices =  []
        downindices = []
        leftindices = []
        rightindices = []
        for idx in range(self.grid_width):
            downindices.append((self.grid_height - 1,idx))
            upindices.append((0,idx))
        for idx in range(self.grid_height):
            leftindices.append ((idx, 0))
            rightindices.append((idx,self.grid_width - 1))
            
        # Here is the end result; a dictionary of lists AND
        # a dictionary of opposites, useful for the move function
        self.directions ={UP:upindices,
                     DOWN:downindices,
                     LEFT:leftindices,
                     RIGHT:rightindices}
        self.directionsopposite ={UP: self.get_grid_width(), 
                                  DOWN: self.get_grid_width(),
                                  RIGHT: self.get_grid_height(), 
                                  LEFT: self.get_grid_height()}
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        for index in range(0, self.grid_height):
            self.grid.append([index - index] * self.grid_width)
        return self.grid
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self.grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height
    
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        #samedirection potentially alters the global variable
        # to either stop or to ensure a new number appears in the grid
        samedirection = 0
        
        #Now, iterate over the first values of our given direction
        for row, col in self.directions[direction]:
            line = []
            values = []
            #Then, iterate over the rows/columns associated with each
            # set of coordinates of our given direction by adding
            # the OFFSET value for each iteration
            while len(line) < ((self.grid_height + self.grid_width) - len(self.directions[direction])):
                line.append((row, col))
                values.append(self.get_tile(row,col))
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
            #Merge the resultant list and place the values back in the grid
            merged = merge(values)
            if merged == values:
                samedirection += 1
            counter = 0
            for index in line:
                    self.set_tile(index[0], index[1], merged[counter])
                    counter += 1
        #Call new_tile as need be
        if samedirection != len(self.directions[direction]):
                                self.new_tile()
            
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #First, randomly create a new set of coordinates
        newnumber = random.randint(0, 10)
        row = random.randint(0, (self.grid_height-1))
        col = random.randint(0, (self.grid_width-1))
        #Check until we find a set of coordinates where the
        #value isn't zero
        while self.grid[row][col] != 0:
            row = random.randint(0, (self.grid_height-1))
            col = random.randint(0, (self.grid_width-1))
        # Ensure the 90%/10% split
        if self.grid[row][col] == 0:
            if newnumber == 9:
                self.grid[row][col] = 4
            else:
                self.grid[row][col] = 2
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """   
        self.grid[row][col] = value
        
    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self.grid[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))