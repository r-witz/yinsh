import socket
import json
import os
from dotenv import load_dotenv
load_dotenv()

class Client:
    def __init__(self, server_address):
        self.SERVER_ADRESS = server_address
        self.SERVER_PORT = int(os.environ.get("PORT"))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.SERVER_ADRESS, self.SERVER_PORT))
        self.your_turn = False

    def fetch_game_state(self):
        try:
            request = {'type': 'fetch'}
            self.client_socket.sendall(json.dumps(request).encode())
            response = json.loads(self.client_socket.recv(4096).decode())
            self.your_turn = response.pop('your_turn')
            return response
        except Exception as e:
            print(f"Failed to fetch game state: {e}")
            return None

    def update_game_state(self, game_state):
        try:
            request = {'type': 'update', 'state': game_state}
            self.client_socket.sendall(json.dumps(request).encode())
            response = json.loads(self.client_socket.recv(4096).decode())
            return response
        except Exception as e:
            print(f"Failed to update game state: {e}")
            return None