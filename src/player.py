from hexagone import Hexagone

class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.rings = []
        self.alignment = 0
        self.marker_placed = None

    def place_ring(self, position: tuple[int, int], board: list[list[Hexagone]]) -> None:
        i, j = position
        board[i][j].state = "RING_P" + self.name[-1]  # Assuming player's name is "PlayerX"
        self.rings.append([i, j])
        
    def remove_ring(self, position: tuple[int, int], board: list[list[Hexagone]]) -> None:
        i, j = position
        board[i][j].state = "EMPTY"
        self.rings.remove([i, j])
        
    def place_marker(self, position: tuple[int, int], board: list[list[Hexagone]]) -> None:
        i, j = position
        board[i][j].marker = "MARKER_P" + self.name[-1]  # Assuming player's name is "PlayerX"
    
    def remove_marker(self, position: tuple[int, int], board: list[list[Hexagone]]) -> None:
        i, j = position
        board[i][j].marker = "EMPTY"
        
    def move_ring(self, initial_position: tuple[int, int], final_position: tuple[int, int], board: list[list[Hexagone]]):
        self.remove_ring(initial_position, board)
        self.place_ring(final_position, board)