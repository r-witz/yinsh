import socket
import threading
import json
import os
from dotenv import load_dotenv
import pygame
load_dotenv()

class Network:
    def __init__(self):
        self.SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
        self.SERVER_PORT = int(os.environ.get("PORT"))

        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption("YINSH")
        

        
        
        self.game_state = {
            'board': {"board": [[None, None, None, None, None, None, ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], None],
                                [None, None, None, None, ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"]],
                                [None, None, None, ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"]],
                                [None, None, ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"]],
                                [None, ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"]],
                                [None, ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], None],
                                [["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], None],
                                [["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], None, None],
                                [["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], None, None, None],
                                [["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], None, None, None, None],
                                [None, ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], None, None, None, None, None, None]],
                                "current_player": "X",
                                "winner": None},
        }
        
        self.players = {'player1': None, 'player2': None}

        
        threading.Thread(target=self.run, args=(self.screen,)).start()

    def run(self, screen):
        while True:
            pygame.Clock().tick(60)
            pygame.display.flip()

    def load_game_state(self):
        try:
            with open("game.json", "r") as f:
                self.game_state = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_game_state()

    def save_game_state(self):
        with open("game.json", "w") as f:
            json.dump(self.game_state, f)

    def handle_client(self, conn, addr, player):
        self.players[player] = conn
        print(f"{player} connected by {addr}")

        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                request = json.loads(data.decode())
                if request['type'] == 'fetch':
                    response = self.game_state
                elif request['type'] == 'update':
                    self.game_state.update(request['state'])
                    self.save_game_state()
                    response = {'status': 'success'}
                else:
                    response = {'status': 'error', 'message': 'Invalid request type'}

                conn.sendall(json.dumps(response).encode())
            except Exception as e:
                print(f"Exception: {e}")
                break

        conn.close()
        self.players[player] = None
        print(f"{player} disconnected")

    def start_server(self):
        print(f"server address: {self.SERVER_ADDRESS}")
        print(f"server port: {self.SERVER_PORT}")

        self.load_game_state()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.SERVER_ADDRESS, self.SERVER_PORT))
            s.listen()
            print(f"Server listening on {self.SERVER_ADDRESS}:{self.SERVER_PORT}")

            while True:
                conn, addr = s.accept()

                if self.players['player1'] is None:
                    threading.Thread(target=self.handle_client, args=(conn, addr, 'player1')).start()
                elif self.players['player2'] is None:
                    threading.Thread(target=self.handle_client, args=(conn, addr, 'player2')).start()
                else:
                    conn.sendall(json.dumps({'status': 'error', 'message': 'Both players are connected'}).encode())
                    conn.close()

if __name__ == "__main__":
    network = Network()
    network.start_server()