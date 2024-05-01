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
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.board = Board()

        self.video = cv2.VideoCapture("assets/graphics/background/menu.mp4")
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        self.p1 = Player("Player1", "blue")
        self.p2 = Player("Player2", "red")
        self.player_to_play = self.p1

    def play_video(self, surface):
        success, video_image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, video_image = self.video.read()
        video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
        surface.blit(video_surf, (0, 0))

    def run(self, screen):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # handle all game logic on click (LMAO c'est du caca mais ça marche) 
                    # TODO Clean in functions to handle this
                    mouse_pos = pygame.mouse.get_pos()
                    i, j = self.board.get_hexagon_at_click(mouse_pos)
                    if i is None or j is None:
                        continue
                    
                    selected_hexagon = self.board.board[i][j]
                    rings_placed = len(self.p1.rings) == 5 and len(self.p2.rings) == 5
                    if rings_placed:
                        move = self.player_to_play.place_marker(selected_hexagon)
                    else:
                        move = self.player_to_play.place_ring(selected_hexagon)

                    if move:
                        self.board.board[i][j] == move
                        self.player_to_play = self.p1 if self.player_to_play == self.p2 else self.p2


            self.clock.tick(self.fps)

            self.play_video(screen)
            surface_board = self.board.draw_board()
            surface_board = self.board.draw_player_elements(surface_board)
            screen.blit(surface_board, (0, 0))

            pygame.display.flip()

if __name__ == "__main__":
    Game().run(screen)