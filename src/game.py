import pygame # type: ignore
import cv2 # type: ignore
from sys import exit
from math import sqrt

from player import Player
from board import Board

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
pygame.display.set_caption("YINSH")

class Game:
    def __init__(self, gamemode: str, difficulty: str) -> None:
        self.clock = pygame.time.Clock()

        self.gamemode = gamemode # AI, Local, Online
        self.difficulty = difficulty # Normal, Blitz

        self.alignement_to_win = 1 if self.difficulty == "Blitz" else 3

        self.video = cv2.VideoCapture("assets/graphics/background/menu.mp4")
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        self.board = Board()
        self.p1 = Player("Player1")
        self.p2 = Player("Player2")
        self.player_to_play = self.p1

    def play_background_music(self):
        pygame.mixer.music.load("assets/audio/piano-loop-3.mp3")
        pygame.mixer.music.play(-1)

    def game_turn(self):
        mouse_pos = pygame.mouse.get_pos()
        i, j = self.board.get_hexagon_at_click(mouse_pos)
        if i is None and j is None:
            return None
        
        player_to_play_name = self.player_to_play.name
        clicked_hex = self.board.board[i][j]
        are_rings_placed = len(self.p1.rings) == 5 and len(self.p2.rings) == 5 and self.p1.alignment == 0 and self.p2.alignment == 0
        
        if are_rings_placed:
            # Place marker
            if self.player_to_play.marker_placed is None and clicked_hex.state == "RING_P" + player_to_play_name[-1]:
                self.player_to_play.place_marker((i, j), self.board.board)
                self.player_to_play.marker_placed = (i, j)
            # Move ring
            elif self.player_to_play.marker_placed:
                i_marker, j_marker = self.player_to_play.marker_placed
                valid_moves = self.board.valid_moves(i_marker, j_marker)

                # If the clicked hex is a valid move, move the ring
                if (i, j) in valid_moves:
                    self.player_to_play.move_ring((i_marker, j_marker), (i, j), self.board.board)
                    self.board.flip_markers(i_marker, j_marker, i, j)

                    self.player_to_play.marker_placed = None
                    self.player_to_play = self.p2 if self.player_to_play == self.p1 else self.p1

        else:
            if clicked_hex.state == "EMPTY":
                self.player_to_play.place_ring((i, j), self.board.board)
                self.player_to_play = self.p2 if self.player_to_play == self.p1 else self.p1

    def get_inputs(self):
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

        while True:
            self.clock.tick(self.fps)
            
            self.get_inputs()
            self.play_background_video(screen)
            self.draw_board(screen)

            pygame.display.flip()

if __name__ == "__main__":
    Game("Local", "Normal").run(screen)