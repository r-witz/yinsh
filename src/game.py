import pygame
import cv2

from sys import exit
from random import choice, randint

from player import Player
from board import Board
from hexagon import Hexagon

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
pygame.display.set_caption("YINSH")

class Game:
    def __init__(self, gamemode: str, difficulty: str) -> None:
        """
        Initialize the Game class
        :param gamemode: str, the game mode (AI, Local, Online)
        :param difficulty: str, the game difficulty (Normal, Blitz)
        """
        self.clock = pygame.time.Clock()

        self.gamemode = gamemode
        self.difficulty = difficulty
        self.alignement_to_win = 1 if self.difficulty == "Blitz" else 3

        self.board = Board()
        self.p1 = Player("Player1")
        self.p2 = Player("Player2")
        self.player_to_play = self.p1
        self.rings_placed = False

        self.video = cv2.VideoCapture("assets/graphics/background/menu.mp4")
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        # Load title image
        self.title = pygame.image.load("assets/graphics/logo/Yinsh.png")
        self.title = self.title.convert_alpha()
        self.title = pygame.transform.scale(self.title, (374, 96))

        # Load rings images for scores
        self.empty_ring = pygame.image.load("assets/graphics/rings/RING_EMPTY.png")
        self.ring_p1 = pygame.image.load("assets/graphics/rings/RING_P1.png")
        self.ring_p2 = pygame.image.load("assets/graphics/rings/RING_P2.png")
        self.empty_ring = self.empty_ring.convert_alpha()
        self.ring_p1 = self.ring_p1.convert_alpha()
        self.ring_p2 = self.ring_p2.convert_alpha()
        self.empty_ring = pygame.transform.scale(self.empty_ring, (100, 100))
        self.ring_p1 = pygame.transform.scale(self.ring_p1, (100, 100))
        self.ring_p2 = pygame.transform.scale(self.ring_p2, (100, 100))

    def has_won(self, player: Player) -> bool:
        """
        Check if a player has won the game
        :param player: Player, the player to check
        :return: bool, True if the player has won, False otherwise
        """
        return player.alignment == self.alignement_to_win

    def play_background_music(self) -> None:
        """
        Play the background music for the game
        """
        pygame.mixer.music.load("assets/audio/piano-loop-3.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0)

    def bot_turn(self) -> None:
        """
        Handle the AI's turn in the game
        """
        if self.rings_placed:
            self.place_marker_and_move_ring()
        else:
            self.place_ring()
        self.switch_player()

    def place_ring(self) -> None:
        """
        Place a ring on the board during the AI's turn
        """
        while True:
            i = randint(0, 10)
            j = randint(0, 10)
            if self.board.board[i][j] is not None and self.board.board[i][j].state == "EMPTY":
                self.player_to_play.place_ring((i, j), self.board.board)
                break
        self.check_if_rings_placed()

    def check_if_rings_placed(self) -> None:
        """
        Check if all rings have been placed on the board
        """
        if len(self.p1.rings) == 5 and len(self.p2.rings) == 5:
            self.rings_placed = True

    def place_marker_and_move_ring(self) -> None:
        """
        Place a marker and move a ring on the board during the AI's turn
        """
        choosen_ring = choice(self.player_to_play.rings)
        i, j = choosen_ring
        self.player_to_play.place_marker((i, j), self.board.board)
        valid_moves = self.board.valid_moves(i, j)
        choosen_move = choice(valid_moves)
        self.player_to_play.move_ring((i, j), choosen_move, self.board.board)
        self.board.flip_markers(i, j, choosen_move[0], choosen_move[1])

    def switch_player(self) -> None:
        """
        Switch the current player to the other player
        """
        self.player_to_play = self.p2 if self.player_to_play == self.p1 else self.p1

    def game_turn(self) -> None:
        """
        Handle a player's turn during the game
        """
        mouse_pos = pygame.mouse.get_pos()
        i, j = self.board.get_hexagon_at_click(mouse_pos)
        if i is None and j is None:
            return None
        self.handle_player_turn(i, j)

    def handle_player_turn(self, i: int, j: int) -> None:
        """
        Handle the actions a player can perform during their turn
        :param i: int, the row index of the clicked hexagon
        :param j: int, the column index of the clicked hexagon
        """
        player_to_play_name = self.player_to_play.name
        clicked_hex = self.board.board[i][j]
        if not self.rings_placed:
            self.handle_ring_placement(i, j, clicked_hex)
        else:
            self.handle_marker_placement_and_ring_movement(i, j, player_to_play_name, clicked_hex)

    def handle_ring_placement(self, i: int, j: int, clicked_hex: Hexagon) -> None:
        """
        Handle the placement of a ring on the board
        :param i: int, the row index of the clicked hexagon
        :param j: int, the column index of the clicked hexagon
        :param clicked_hex: Hexagon, the clicked hexagon
        """
        if clicked_hex.state == "EMPTY":
            self.player_to_play.place_ring((i, j), self.board.board)
            self.check_if_rings_placed()
            self.switch_player()

    def handle_marker_placement_and_ring_movement(self, i: int, j: int, player_to_play_name: str, clicked_hex: Hexagon) -> None:
        """
        Handle the placement of a marker and the movement of a ring on the board
        :param i: int, the row index of the clicked hexagon
        :param j: int, the column index of the clicked hexagon
        :param player_to_play_name: str, the name of the current player
        :param clicked_hex: Hexagon, the clicked hexagon
        """
        if self.player_to_play.marker_placed is None and clicked_hex.state == "RING_P" + player_to_play_name[-1]:
            self.player_to_play.place_marker((i, j), self.board.board)
            self.player_to_play.marker_placed = (i, j)
        elif self.player_to_play.marker_placed:
            self.handle_ring_movement(i, j)

    def handle_ring_movement(self, i: int, j: int) -> None:
        """
        Handle the movement of a ring on the board
        :param i: int, the row index of the clicked hexagon
        :param j: int, the column index of the clicked hexagon
        """
        i_marker, j_marker = self.player_to_play.marker_placed
        valid_moves = self.board.valid_moves(i_marker, j_marker)
        if (i, j) in valid_moves:
            self.player_to_play.move_ring((i_marker, j_marker), (i, j), self.board.board)
            self.board.flip_markers(i_marker, j_marker, i, j)
            self.player_to_play.marker_placed = None
            self.switch_player()

    def get_inputs(self) -> None:
        """
        Get the inputs from the user during the game
        """
        if self.gamemode == "AI" and self.player_to_play == self.p2:
            self.bot_turn()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_turn()

    def play_background_video(self, surface: pygame.Surface) -> None:
        """
        Play the background video for the game
        :param surface: pygame.Surface, the surface to display the video on
        """
        success, video_image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, video_image = self.video.read()
        video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
        surface.blit(video_surf, (0, 0))

    def draw_score(self, screen: pygame.Surface) -> None:
        """
        Draw the score of the game on the screen
        :param screen: pygame.Surface, the surface to display the score on
        """
        for i in range(self.alignement_to_win):
            screen.blit(self.empty_ring, (900 + i * 120, 950))

        for i in range(self.p1.alignment):
            screen.blit(self.ring_p1, (900 + i * 120, 950))

        for i in range(self.alignement_to_win):
            screen.blit(self.empty_ring, (1750 - i * 120, 950))

        for i in range(self.p2.alignment):
            screen.blit(self.ring_p2, (1750 - i * 120, 950))

    def draw_ui(self, screen: pygame.Surface) -> None:
        """
        Draw the UI on the screen
        :param screen: pygame.Surface, the surface to display the UI on
        """
        screen.blit(self.title, (375, 90))
        self.draw_score(screen)

    def draw_board(self, screen: pygame.Surface) -> None:
        """
        Draw the game board on the screen
        :param screen: pygame.Surface, the surface to display the board on
        """
        surface_board = self.board.draw_board()
        surface_board = self.board.draw_player_elements(surface_board)
        screen.blit(surface_board, (0, 0))

    def run(self, screen: pygame.Surface) -> None:
        """
        Run the game loop
        :param screen: pygame.Surface, the surface to display the game on
        """
        self.play_background_music()
        while not self.has_won(self.p1) and not self.has_won(self.p2):
            self.clock.tick(self.fps)
            self.get_inputs()
            self.play_background_video(screen)
            self.draw_ui(screen)
            self.draw_board(screen)
            pygame.display.flip()

if __name__ == "__main__":
    Game("AI", "Normal").run(screen)