class Cell:
    def __init__(self, row: int, column: int) -> None:
        self.row: int = row
        self.column: int = column
        self.north: bool = True
        self.south: bool = True
        self.east: bool = True
        self.west: bool = True
        self.visited: bool = False
        self.blocked: bool = False
