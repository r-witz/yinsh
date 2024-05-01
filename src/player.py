from hexagone import Hexagone

class Player:
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.rings = []
        self.ring_to_move = None

    def place_ring(self, hexagon: Hexagone) -> Hexagone:
        if hexagon.state == "EMPTY":
            hexagon.state = "RING_P" + self.name[-1]  # Assuming player's name is "PlayerX"
            self.rings.append(hexagon)
            return hexagon
        else:
            return None

    def place_marker(self, hexagon: Hexagone) -> Hexagone:
        if hexagon.state == "RING_P" + self.name[-1]:
            hexagon.marker = "MARKER_P" + self.name[-1]  # Assuming player's name is "PlayerX"
            return hexagon
        else:
            return None
        
    def move_ring(self, hexagon, board):
        pass