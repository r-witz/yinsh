import pygame
import cv2
from sys import exit
from random import choice, randint
from player import Player
from board import Board

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
pygame.display.set_caption("YINSH")

class Game:
    def __init__(self, gamemode: str, difficulty: str) -> None:
        self.clock = pygame.time.Clock()

        self.gamemode = gamemode
        self.difficulty = difficulty
        self.alignement_to_win = 1 if self.difficulty == "Blitz" else 3

        self.video = cv2.VideoCapture("assets/graphics/background/menu.mp4")
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        self.board = Board()
        self.p1 = Player("Player1")
        self.p2 = Player("Player2")
        self.player_to_play = self.p1
        self.rings_placed = False

    def has_won(self, player: Player) -> bool:
        return player.alignment == self.alignement_to_win

    def play_background_music(self):
        pygame.mixer.music.load("assets/audio/piano-loop-3.mp3")
        pygame.mixer.music.play(-1)

    def bot_turn(self):
        if self.rings_placed:
            self.place_marker_and_move_ring()
        else:
            self.place_ring()

    def place_ring(self):
        while True:
            i = randint(0, 10)
            j = randint(0, 10)
            if self.board.board[i][j].state == "EMPTY":
                self.player_to_play.place_ring((i, j), self.board.board)
                break
        self.check_if_rings_placed()

    def check_if_rings_placed(self):
        if len(self.p1.rings) == 5 and len(self.p2.rings) == 5:
            self.rings_placed = True

    def place_marker_and_move_ring(self):
        choosen_ring = choice(self.player_to_play.rings)
        i, j = choosen_ring
        self.player_to_play.place_marker((i, j), self.board.board)
        valid_moves = self.board.valid_moves(i, j)
        choosen_move = choice(valid_moves)
        self.player_to_play.move_ring((i, j), choosen_move, self.board.board)
        self.board.flip_markers(i, j, choosen_move[0], choosen_move[1])
        self.switch_player()

    def switch_player(self):
        self.player_to_play = self.p2 if self.player_to_play == self.p1 else self.p1

    def game_turn(self):
        mouse_pos = pygame.mouse.get_pos()
        i, j = self.board.get_hexagon_at_click(mouse_pos)
        if i is None and j is None:
            return None
        self.handle_player_turn(i, j)

    def handle_player_turn(self, i, j):
        player_to_play_name = self.player_to_play.name
        clicked_hex = self.board.board[i][j]
        if not self.rings_placed:
            self.handle_ring_placement(i, j, clicked_hex)
        else:
            self.handle_marker_placement_and_ring_movement(i, j, player_to_play_name, clicked_hex)

    def handle_ring_placement(self, i, j, clicked_hex):
        if clicked_hex.state == "EMPTY":
            self.player_to_play.place_ring((i, j), self.board.board)
            self.check_if_rings_placed()
            self.switch_player()

    def handle_marker_placement_and_ring_movement(self, i, j, player_to_play_name, clicked_hex):
        if self.player_to_play.marker_placed is None and clicked_hex.state == "RING_P" + player_to_play_name[-1]:
            self.player_to_play.place_marker((i, j), self.board.board)
            self.player_to_play.marker_placed = (i, j)
        elif self.player_to_play.marker_placed:
            self.handle_ring_movement(i, j)

    def handle_ring_movement(self, i, j):
        i_marker, j_marker = self.player_to_play.marker_placed
        valid_moves = self.board.valid_moves(i_marker, j_marker)
        if (i, j) in valid_moves:
            self.player_to_play.move_ring((i_marker, j_marker), (i, j), self.board.board)
            self.board.flip_markers(i_marker, j_marker, i, j)
            self.player_to_play.marker_placed = None
            self.switch_player()

    def get_inputs(self):
        if self.gamemode == "AI" and self.player_to_play == self.p2:
            self.bot_turn()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_turn()

    def play_background_video(self, surface):
        success, video_image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, video_image = self.video.read()
        video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
        surface.blit(video_surf, (0, 0))

    def draw_board(self, screen):
        surface_board = self.board.draw_board()
        surface_board = self.board.draw_player_elements(surface_board)
        screen.blit(surface_board, (0, 0))

    def run(self, screen):
        self.play_background_music()
        while not self.has_won(self.p1) and not self.has_won(self.p2):
            self.clock.tick(self.fps)
            self.get_inputs()
            self.play_background_video(screen)
            self.draw_board(screen)
            pygame.display.flip()

if __name__ == "__main__":
    Game("AI", "Normal").run(screen)