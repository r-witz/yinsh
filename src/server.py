import socket
import threading
import json
import os
from dotenv import load_dotenv
load_dotenv()

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"Failed to get local IP: {e}")
        return '127.0.0.1'

class Server:
    def __init__(self):
        self.SERVER_ADDRESS = get_local_ip()
        self.SERVER_PORT = int(os.environ.get("PORT"))
        
        self.game_state = {"board": [[None, None, None, None, None, None, ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], ["EMPTY", "EMPTY"], None],
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
                            "current_player": "1",
                            "winner": None,
                            "p1_rings": [],
                            "p2_rings": [],
                            "rings_placed": False,
                            "p1_alignement": "0",
                            "p2_alignement": "0",
                            "alignement_to_win": "3"
                            }

        self.players = {'Player1': None, 'Player2': None}

    def handle_client(self, conn, addr, player):
        print(f"Player {player} connected by {addr}")

        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                request = json.loads(data.decode())
                if request['type'] == 'fetch':
                    response = self.game_state.copy()
                    response['your_turn'] = (self.game_state['current_player'] == str(player))
                elif request['type'] == 'update':
                    if self.game_state['current_player'] == str(player):
                        self.game_state = request['state']
                    response = {'status': 'success'}
                else:
                    response = {'status': 'error', 'message': 'Invalid request type'}

                conn.sendall(json.dumps(response).encode())
            except Exception as e:
                print(f"Exception: {e}")
                break

        conn.close()
        self.players["Player"+str(player)] = None
        print(f"Player {player} disconnected")

    def start_server(self):
        print(f"server address: {self.SERVER_ADDRESS}")
        print(f"server port: {self.SERVER_PORT}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.SERVER_ADDRESS, self.SERVER_PORT))
            s.listen(2)
            print(f"Server listening on {self.SERVER_ADDRESS}:{self.SERVER_PORT}")

            while True:
                client_socket, addr = s.accept()
                if self.players["Player1"] is None:
                    self.players["Player1"] = client_socket
                    threading.Thread(target=self.handle_client, args=(client_socket, addr, 1)).start()
                elif self.players["Player2"] is None:
                    self.players["Player2"] = client_socket
                    threading.Thread(target=self.handle_client, args=(client_socket, addr, 2)).start()