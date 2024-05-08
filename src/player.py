from hexagon import Hexagon

class Player:
    def __init__(self, name: str) -> None:
        """
        Initialize the Player class
        :param name: str, the name of the player (e.g., "Player1", "Player2")
        """
        self.name = name
        self.rings = []
        self.alignment = 0
        self.marker_placed = None

    def place_ring(self, position: tuple[int, int], board: list[list[Hexagon]]) -> None:
        """
        Place a ring on the board at the specified position
        :param position: tuple[int, int], the position to place the ring at
        :param board: list[list[Hexagon]], the game board
        """
        i, j = position
        board[i][j].state = "RING_P" + self.name[-1]  # Assuming player's name is "PlayerX"
        self.rings.append([i, j])
        
    def remove_ring(self, position: tuple[int, int], board: list[list[Hexagon]]) -> None:
        """
        Remove a ring from the board at the specified position
        :param position: tuple[int, int], the position to remove the ring from
        :param board: list[list[Hexagon]], the game board
        """
        i, j = position
        board[i][j].state = "EMPTY"
        self.rings.remove([i, j])
        
    def place_marker(self, position: tuple[int, int], board: list[list[Hexagon]]) -> None:
        """
        Place a marker on the board at the specified position
        :param position: tuple[int, int], the position to place the marker at
        :param board: list[list[Hexagon]], the game board
        """
        i, j = position
        board[i][j].marker = "MARKER_P" + self.name[-1]  # Assuming player's name is "PlayerX"
    
    def remove_marker(self, position: tuple[int, int], board: list[list[Hexagon]]) -> None:
        """
        Remove a marker from the board at the specified position
        :param position: tuple[int, int], the position to remove the marker from
        :param board: list[list[Hexagon]], the game board
        """
        i, j = position
        board[i][j].marker = "EMPTY"
        
    def move_ring(self, initial_position: tuple[int, int], final_position: tuple[int, int], board: list[list[Hexagon]]):
        """
        Move a ring from the initial position to the final position on the board
        :param initial_position: tuple[int, int], the initial position of the ring
        :param final_position: tuple[int, int], the final position of the ring
        :param board: list[list[Hexagon]], the game board
        """
        self.remove_ring(initial_position, board)
        self.place_ring(final_position, board)