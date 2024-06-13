import pygame
import cv2

from sys import exit
from random import choice, randint
from json import load

from src.player import Player
from src.board import Board
from src.hexagon import Hexagon
from src.client import Client
from src.resizing import Resizer

class Game:
    def __init__(self, gamemode: str, difficulty: str, ip: str = None) -> None:
        """
        Initialize the Game class
        :param gamemode: str, the game mode (AI, Local, Online)
        :param difficulty: str, the game difficulty (Normal, Blitz)
        """
        self.clock = pygame.time.Clock()

        self.ip = ip
        self.client = Client(self.ip) if gamemode == "Online" else None

        self.gamemode = gamemode
        self.difficulty = difficulty
        self.alignement_to_win = 1 if self.difficulty == "Blitz" else 3

        self.board = Board()
        self.p1 = Player("Player1")
        self.p2 = Player("Player2")
        self.player_to_play = self.p1
        self.rings_placed = False
        self.ring_removal = False
        self.alignements = None
        self.alignement_player = None
        self.winner = None

        self.settings = False
        self.video = cv2.VideoCapture("assets/graphics/background/menu.mp4")
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        self.load_images()

        if Client:
            self.send_game_infos()

    def load_images(self) -> None:
        """
        Load the images for the game
        """
        # Load title image
        self.title = pygame.image.load("assets/graphics/logo/Yinsh.png").convert_alpha()
        self.title = pygame.transform.scale(self.title, (374, 96))

        # Load rings images for scores
        self.empty_ring = pygame.image.load("assets/graphics/rings/RING_EMPTY.png").convert_alpha()
        self.ring_p1 = pygame.image.load("assets/graphics/rings/RING_P1.png").convert_alpha()
        self.ring_p2 = pygame.image.load("assets/graphics/rings/RING_P2.png").convert_alpha()
        self.empty_ring = pygame.transform.scale(self.empty_ring, (100, 100))
        self.ring_p1 = pygame.transform.scale(self.ring_p1, (100, 100))
        self.ring_p2 = pygame.transform.scale(self.ring_p2, (100, 100))

        # Load indicators images
        self.blue_place_ring = pygame.image.load("assets/graphics/indicators/BLUE_PLACE_RING.png").convert_alpha()
        self.blue_put_marker = pygame.image.load("assets/graphics/indicators/BLUE_PLACE_MARKER.png").convert_alpha()
        self.blue_move_ring = pygame.image.load("assets/graphics/indicators/BLUE_MOVE_RING.png").convert_alpha()
        self.blue_remove_ring = pygame.image.load("assets/graphics/indicators/BLUE_REMOVE_RING.png").convert_alpha()
        self.blue_remove_alignement = pygame.image.load("assets/graphics/indicators/BLUE_REMOVE_ALIGNEMENT.png").convert_alpha()
        self.red_place_ring = pygame.image.load("assets/graphics/indicators/RED_PLACE_RING.png").convert_alpha()
        self.red_put_marker = pygame.image.load("assets/graphics/indicators/RED_PLACE_MARKER.png").convert_alpha()
        self.red_move_ring = pygame.image.load("assets/graphics/indicators/RED_MOVE_RING.png").convert_alpha()
        self.red_remove_ring = pygame.image.load("assets/graphics/indicators/RED_REMOVE_RING.png").convert_alpha()
        self.red_remove_alignement = pygame.image.load("assets/graphics/indicators/RED_REMOVE_ALIGNEMENT.png").convert_alpha()
        self.blue_place_ring = pygame.transform.scale(self.blue_place_ring, (950, 100))
        self.blue_put_marker = pygame.transform.scale(self.blue_put_marker, (950, 100))
        self.blue_move_ring = pygame.transform.scale(self.blue_move_ring, (950, 100))
        self.blue_remove_ring = pygame.transform.scale(self.blue_remove_ring, (950, 100))
        self.blue_remove_alignement = pygame.transform.scale(self.blue_remove_alignement, (950, 100))
        self.red_place_ring = pygame.transform.scale(self.red_place_ring, (950, 100))
        self.red_put_marker = pygame.transform.scale(self.red_put_marker, (950, 100))
        self.red_move_ring = pygame.transform.scale(self.red_move_ring, (950, 100))
        self.red_remove_ring = pygame.transform.scale(self.red_remove_ring, (950, 100))
        self.red_remove_alignement = pygame.transform.scale(self.red_remove_alignement, (950, 100))

        self.load_assets = Resizer(1920, 1080).load_assets
        self.menu_button, self.menu_button_rect = self.load_assets()['menu_button']
        self.resume_button, self.resume_button_rect = self.load_assets()['resume_button']
        
        self.resume_button, self.menu_button = (
            pygame.transform.scale(self.resume_button, (400, 125)), 
            pygame.transform.scale(self.menu_button, (400, 125))
        )

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
        with open('settings.json', 'r') as f:
            settings = load(f)
        pygame.mixer.music.set_volume(settings['volumes']['music'])

    def update_music_volume(self) -> None:
        """
        Update the volume of the music
        """
        pass
        
    def check_if_rings_placed(self) -> None:
        """
        Check if all rings have been placed on the board
        """
        if len(self.p1.rings) == 5 and len(self.p2.rings) == 5:
            self.rings_placed = True

    def switch_player(self) -> None:
        """
        Switch the current player to the other player
        """
        self.player_to_play = self.p2 if self.player_to_play == self.p1 else self.p1

    def bot_turn(self) -> None:
        """
        Handle the AI's turn during the game
        """
        if not self.rings_placed:
            self.wait(1000)
            self.bot_place_ring()
        else:
            self.wait(1000)
            self.bot_marker_placement_and_ring_movement()
    
    def bot_place_ring(self) -> None:
        """
        Handle the AI's ring placement during the game
        """
        while True:
            i = randint(0, 10)
            j = randint(0, 10)
            if self.board.board[i][j] is not None and self.board.board[i][j].state == "EMPTY":
                self.p2.place_ring((i, j), self.board.board)
                break
        self.check_if_rings_placed()
        self.switch_player()

    def bot_marker_placement_and_ring_movement(self) -> None:
        """
        Handle the AI's marker placement and ring movement during the game
        """
        choosen_ring = choice(self.player_to_play.rings)
        i, j = choosen_ring
        self.player_to_play.place_marker((i, j), self.board.board)
        self.player_to_play.marker_placed = (i, j)
        self.wait(500)
        valid_moves = self.board.valid_moves(i, j)
        if valid_moves == []:
            self.winner = self.p1.name
            return
        choosen_move = choice(valid_moves)
        self.player_to_play.move_ring((i, j), choosen_move, self.board.board)
        self.board.flip_markers(i, j, choosen_move[0], choosen_move[1])
        self.player_to_play.marker_placed = None
        self.switch_player()

    def bot_alignement_removal(self) -> None:
        """
        Handle the AI's alignement removal during the game
        """
        self.wait(1000)
        alignement = choice(self.alignements)
        for i, j in alignement:
            self.board.board[i][j].marker = "EMPTY"
        self.ring_removal = True
        self.wait(1000)
        i, j = choice(self.p2.rings)
        self.p2.remove_ring((i, j), self.board.board)
        self.alignements = None
        self.ring_removal = False
        self.p2.alignment += 1

        if self.has_won(self.p2):
            self.winner = self.p2.name
            return
        
        if not self.check_alignements(self.p2):
            if self.alignement_player:
                self.check_alignements(self.alignement_player)

    def game_turn(self) -> None:
        """
        Handle a player's turn during the game
        """
        mouse_pos = pygame.mouse.get_pos()
        i, j = self.board.get_hexagon(mouse_pos)
        if i is None and j is None:
            return None
        self.player_turn(i, j)

    def player_turn(self, i: int, j: int) -> None:
        """
        Handle the actions a player can perform during their turn
        :param i: int, the row index of the clicked hexagon
        :param j: int, the column index of the clicked hexagon
        """
        clicked_hex = self.board.board[i][j]
        if not self.rings_placed:
            self.ring_placement(i, j, clicked_hex)
        elif self.ring_removal:
            self.remove_ring(i, j, self.alignement_player)
        elif self.alignements is not None:
            self.remove_alignement(i, j, self.alignement_player)
        else:
            self.marker_placement_and_ring_movement(i, j, self.player_to_play.name, clicked_hex)

    def ring_placement(self, i: int, j: int, clicked_hex: Hexagon) -> None:
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

    def check_alignements(self, player: Player) -> bool:
        """
        Check if a player has made an alignment
        :param player: Player, the player to check
        :return: bool, True if the player has made an alignment, False otherwise
        """
        alignements = self.board.check_win(player.name)
        if alignements:
            self.alignements = alignements
            self.alignement_player = player
            return True
        
        if self.alignement_player == self.player_to_play:
            self.alignement_player = self.p1 if self.alignement_player == self.p2 else self.p2
            self.check_alignements(self.alignement_player)
        else:
            self.alignement_player = None
            self.alignements = None
            self.switch_player()
        
        return False

    def get_possible_alignement(self, i: int, j: int) -> list[tuple[int, int]]:
        """
        Get the alignement of a marker
        :param i: int, the row index of the marker
        :param j: int, the column index of the marker
        :return: list, the alignement of the marker
        """
        if self.alignements is None:
            return None
        alignements_possible = [alignement for alignement in self.alignements if (i, j) in alignement]
        if alignements_possible:
            if len(alignements_possible) == 1:
                return alignements_possible[0]
            else:
                for alignement in alignements_possible:
                    if (i, j) == (alignement[2][0], alignement[2][1]):
                        return alignement
                for alignement in alignements_possible:
                    if (i, j) == (alignement[3][0], alignement[3][1]) or (i, j) == (alignement[1][0], alignement[1][1]):
                        return alignement
                for alignement in alignements_possible:
                    if (i, j) == (alignement[4][0], alignement[4][1]) or (i, j) == (alignement[0][0], alignement[0][1]):
                        return alignement
        return None

    def draw_alignement_preview(self, screen: pygame.Surface) -> None:
        """
        If the player hover over a marker of an alignment, show the preview of the alignement selected
        :param screen: pygame.Surface, the surface to display the preview on
        """
        mouse_pos = pygame.mouse.get_pos()
        i, j = self.board.get_hexagon(mouse_pos)
        if i is not None and j is not None:
            alignement = self.get_possible_alignement(i, j)
            if alignement:
                startx, starty = self.board.board[alignement[0][0]][alignement[0][1]].center
                endx, endy = self.board.board[alignement[4][0]][alignement[4][1]].center
                pygame.draw.line(screen, (255, 255, 0), (startx, starty), (endx, endy), 5)
                
    def remove_alignement(self, i: int, j: int, player: Player) -> None:
        """
        Remove an alignement from the board
        :param i: int, the row index of the clicked hexagon
        :param j: int, the column index of the clicked hexagon
        :param player: Player, the player to remove the alignement from
        """
        alignement = self.get_possible_alignement(i, j)
        if alignement:
            for i, j in alignement:
                self.board.board[i][j].marker = "EMPTY"
            self.ring_removal = True
            self.alignements = None
                    
    def remove_ring(self, i: int, j: int, player: Player) -> None:
        """
        Remove a ring from the board
        :param i: int, the row index of the clicked hexagon
        :param j: int, the column index of the clicked hexagon
        :param player: Player, the player to remove the ring from
        """
        if self.board.board[i][j].state == "RING_P" + player.name[-1]:
            player.remove_ring((i, j), self.board.board)
            self.ring_removal = False
            player.alignment += 1

            if self.has_won(player):
                self.winner = player.name
                return
            
            if not self.check_alignements(player):
                if self.alignement_player:
                    self.check_alignements(self.alignement_player)

    def marker_placement_and_ring_movement(self, i: int, j: int, player_to_play_name: str, clicked_hex: Hexagon) -> None:
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
            self.ring_movement(i, j)

    def ring_movement(self, i: int, j: int) -> None:
        """
        Handle the movement of a ring on the board
        :param i: int, the row index of the clicked hexagon
        :param j: int, the column index of the clicked hexagon
        """
        i_marker, j_marker = self.player_to_play.marker_placed
        valid_moves = self.board.valid_moves(i_marker, j_marker)
        if valid_moves == []:
            self.winner = self.p1.name if self.player_to_play == self.p2 else self.p2.name
            return
        
        if (i, j) in valid_moves:
            self.player_to_play.move_ring((i_marker, j_marker), (i, j), self.board.board)
            self.board.flip_markers(i_marker, j_marker, i, j)
            self.player_to_play.marker_placed = None
            
            self.alignement_player = self.player_to_play
            self.check_alignements(self.alignement_player)

    def tab_menu(self, screen: pygame.Surface) -> None:
        """
        Display the tab menu for the game
        :param screen: pygame.Surface, the surface to draw the tab menu on
        """
        self.resume_button_rect.topleft=(755, 410) 
        self.menu_button_rect.topleft = (755, 565)

        pygame.draw.rect(screen, (0, 0, 0), (700, 357, 500, 390), border_radius=30)
        pygame.draw.rect(screen, (249, 240, 194), (700, 357, 500, 390), 7, border_radius=30)
        screen.blit(self.resume_button, self.resume_button_rect)
        screen.blit(self.menu_button, self.menu_button_rect)
            
    def get_inputs(self) -> None:
        """
        Get the inputs from the user during the game
        """
        if self.gamemode == "AI" and self.alignement_player == self.p2:
            self.bot_alignement_removal()
        elif self.gamemode == "AI" and self.player_to_play == self.p2:
            self.bot_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.settings = True if self.settings == False else False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.settings == False and (self.client is None or (self.client is not None and self.client.your_turn)):
                    self.game_turn()
                    self.send_game_infos()
                elif self.settings == True:
                    if self.resume_button_rect.collidepoint(event.pos):
                        self.settings = False
                    if self.menu_button_rect.collidepoint(event.pos):
                        self.settings = False
                        self.winner = "Menu"

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
            screen.blit(self.empty_ring, (900 + i * 120, 810))

        for i in range(self.p1.alignment):
            screen.blit(self.ring_p1, (900 + i * 120, 810))

        for i in range(self.alignement_to_win):
            screen.blit(self.empty_ring, (1750 - i * 120, 810))

        for i in range(self.p2.alignment):
            screen.blit(self.ring_p2, (1750 - i * 120, 810))
            
    def draw_indicators(self, screen: pygame.Surface) -> None:
        """
        Draw the indicators for the player on the screen
        :param screen: pygame.Surface, the surface to display the indicators on
        """
        if not self.rings_placed:
            if self.player_to_play == self.p1:
                screen.blit(self.blue_place_ring, (900, 930))
            else:
                screen.blit(self.red_place_ring, (900, 930))
        elif self.ring_removal:
            if self.alignement_player == self.p1:
                screen.blit(self.blue_remove_ring, (900, 930))
            else:
                screen.blit(self.red_remove_ring, (900, 930))
        elif self.alignements is not None:
            if self.alignement_player == self.p1:
                screen.blit(self.blue_remove_alignement, (900, 930))
            else:
                screen.blit(self.red_remove_alignement, (900, 930))
        else:
            if self.player_to_play == self.p1:
                if self.player_to_play.marker_placed is None:
                    screen.blit(self.blue_put_marker, (900, 930))
                else:
                    screen.blit(self.blue_move_ring, (900, 930))
            else:
                if self.player_to_play.marker_placed is None:
                    screen.blit(self.red_put_marker, (900, 930))
                else:
                    screen.blit(self.red_move_ring, (900, 930))

    def draw_ui(self, screen: pygame.Surface) -> None:
        """
        Draw the UI on the screen
        :param screen: pygame.Surface, the surface to display the UI on
        """
        screen.blit(self.title, (375, 90))
        self.draw_score(screen)
        self.draw_alignement_preview(screen)
        self.draw_indicators(screen)
        if self.settings:
            self.tab_menu(screen)

    def draw_move_preview(self, screen: pygame.Surface) -> None:
        """
        Draw a preview of the possible moves for the player
        :param screen: pygame.Surface, the surface to display the preview on
        """
        if self.player_to_play.marker_placed is not None:
            i, j = self.player_to_play.marker_placed
            valid_moves = self.board.valid_moves(i, j)
            for move in valid_moves:
                x, y = self.board.board[move[0]][move[1]].center
                pygame.draw.circle(screen, (100, 100, 100), (x, y), 14)

    def draw_board(self, screen: pygame.Surface) -> None:
        """
        Draw the game board on the screen
        :param screen: pygame.Surface, the surface to display the board on
        """
        surface_board = self.board.draw_board()
        surface_board = self.board.draw_player_elements(surface_board)
        self.draw_move_preview(surface_board)
        screen.blit(surface_board, (0, 0))
        
    def wait(self, time) -> None:
        """
        Wait for a certain amount of time before continuing the game without stopping the background video and music from playing
        :param time: int, the time to wait in milliseconds
        """
        screen = pygame.display.get_surface()
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < time:
            self.play_background_video(screen)
            self.draw_board(screen)
            self.draw_ui(screen)
            pygame.display.flip()

    def fetch_game_infos(self) -> None:
        """
        Fetch the infos from the server using the connection through the client.
        """
        if self.client is None:
            return
        
        response = self.client.fetch_game_state()
        if response is None: return
        self.board.update_board(response["board"])
        self.player_to_play = self.p1 if response["current_player"] == "1" else self.p2
        self.winner = response["winner"]
        self.p1.rings = response["p1_rings"]
        self.p2.rings = response["p2_rings"]
        self.rings_placed = response["rings_placed"]
        self.p1.alignment = int(response['p1_alignement'])
        self.p2.alignment = int(response['p2_alignement'])
        self.alignement_to_win = int(response['alignement_to_win'])

    def format_game_infos(self) -> dict:
        """
        Format the game's infos to send it to the server through the client.
        :return: dict, The game's informations in json format to send through the client.
        """
        return {
            'board': self.board.board_state(),
            'current_player': "1" if self.player_to_play == self.p1 else "2",
            'winner': self.winner,
            'p1_rings': self.p1.rings,
            'p2_rings': self.p2.rings,
            'rings_placed': self.rings_placed,
            'p1_alignement': self.p1.alignment,
            'p2_alignement': self.p2.alignment,
            'alignement_to_win': self.alignement_to_win
        }

    def send_game_infos(self):
        if self.client:
            game_state = self.format_game_infos()
            response = self.client.update_game_state(game_state)
            if response is not None and response['status'] == 'success':
                self.client.fetch_game_state()
            else:
                print("Failed to send game info")

    def run(self, screen: pygame.Surface) -> None:
        """
        Run the game loop
        :param screen: pygame.Surface, the surface to display the game on
        """
        self.play_background_music()
        while not self.winner:
            self.fetch_game_infos()
            self.clock.tick(self.fps)
            self.play_background_video(screen)
            self.get_inputs()
            self.update_music_volume()
            self.draw_board(screen)
            self.draw_ui(screen)
            pygame.display.flip()

        return self.winner
