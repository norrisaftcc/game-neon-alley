class Cell:
    """
    Cell represents a single cell in the maze.
    It tracks its position and connections to neighboring cells.
    """
    # Direction constants
    NORTH = 1
    SOUTH = 2
    EAST = 4
    WEST = 8
    
    # Direction opposites
    OPPOSITES = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }
    
    def __init__(self, row, col):
        """Initialize a new cell at the given row and column position."""
        self.row = row
        self.col = col
        self.links = 0  # Bitwise flags for linked directions
    
    def linked(self, direction):
        """Check if this cell is linked in the given direction."""
        return (self.links & direction) != 0
    
    def link(self, direction):
        """Link this cell in the given direction."""
        self.links |= direction
    
    def unlink(self, direction):
        """Unlink this cell from the given direction."""
        self.links &= ~direction
    
    def get_links(self):
        """Get a list of all directions where this cell has links."""
        links = []
        if self.linked(Cell.NORTH): links.append(Cell.NORTH)
        if self.linked(Cell.SOUTH): links.append(Cell.SOUTH)
        if self.linked(Cell.EAST): links.append(Cell.EAST)
        if self.linked(Cell.WEST): links.append(Cell.WEST)
        return links