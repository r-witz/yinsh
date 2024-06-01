import socket
import threading
import json
import os
from dotenv import load_dotenv
import pygame
import sys
load_dotenv()

from src.game import Game

class Client:
    def __init__(self):
        self.SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
        self.SERVER_PORT = int(os.environ.get("PORT"))

        self.game = Game("Local", "Normal")

        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption("YINSH")
        # pygame.display init




        self.game_state = {
            'board': self.game.board.board_state(),
            'current_player': 'X',
            'winner': None
        }

        threading.Thread(target=self.launch_game, args=(self.screen,)).start()

        # Initialize socket for communication
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.SERVER_ADDRESS, self.SERVER_PORT))

    def launch_game(self, screen):
        while True:
            pygame.init()
            self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
            pygame.Clock().tick(60)
            self.game.run(self.screen)
            pygame.display.flip()

    def fetch_game_state(self):
        request = {'type': 'fetch'}
        self.client_socket.sendall(json.dumps(request).encode())
        response = json.loads(self.client_socket.recv(4096).decode())
        self.game_state = response

    def update_game_state(self):
        request = {'type': 'update', 'state': self.game_state}
        self.client_socket.sendall(json.dumps(request).encode())
        response = json.loads(self.client_socket.recv(4096).decode())
        return response

    def close_connection(self):
        self.client_socket.close()

    def run(self):
        running = True
        while running:
            self.fetch_game_state()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_state['game_over'] and self.game_state['current_player'] == 'X':
                    
                    self.game_state['board'] = self.game.board.board_state()
                    if self.game_state['board'] == 'EMPTY':
                        self.game_state['current_player'] = 'O'
                        self.update_game_state()
                        if self.game.has_won() == True:
                            self.game_state['winner'] = self.game_state['current_player']

                    elif self.game_state['board'] == 'RING_P1':
                        self.game_state['current_player'] = 'O'
                        self.update_game_state()
                        if self.game.has_won() == True:
                            self.game_state['winner'] = self.game_state['current_player']

                if self.game_state['winner'] == 'X':
                    print("Player 1 wins!")
                    running = False
                elif self.game_state['winner'] == 'O':
                    print("Player 2 wins!")
                    running = False

# Example usage
if __name__ == "__main__":
    client = Client()
    client.run()