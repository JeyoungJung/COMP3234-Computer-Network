import socket
import threading
import random


class GameServer:
    def __init__(self, host="localhost", port=4003):
        with open("UserInfo.txt", "r") as f:
            credentials_list = [line.strip().split(":") for line in f]
        self.credentials = {
            username: password for username, password in credentials_list
        }
        # room's key is the room number and the value is a tuple composed of (client socket info, username)
        self.rooms = {0: [], 1: [], 2: [], 3: [], 4: []}
        self.guesses = {0: [], 1: [], 2: [], 3: [], 4: []}

        self.rooms_lock = threading.Lock()
        self.guesses_lock = threading.Lock()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

    def broadcast(self, room_number, message):
        # Send a message to all clients in a room
        for client, username in self.rooms[room_number]:
            client.send(message.encode())

    def handle_client(self, client):
        try:
            client.send("Please input your user name: ".encode())
            username = client.recv(1024).decode()

            client.send("Please input your password: ".encode())
            password = client.recv(1024).decode()

            if username in self.credentials and self.credentials[username] == password:
                client.send("1001 Authentication successful".encode())
                while True:
                    command = client.recv(1024).decode()
                    if command.startswith("/list"):
                        with self.rooms_lock:
                            message = "3001 " + str(len(self.rooms))
                            for room_number, players in self.rooms.items():
                                message += " " + str(len(players))
                            client.send(message.encode())
                    elif command.startswith("/enter"):
                        room_number = int(command.split(" ")[1])
                        with self.rooms_lock:
                            if len(self.rooms[room_number]) < 2:
                                self.rooms[room_number].append((client, username))
                                if len(self.rooms[room_number]) == 2:
                                    self.broadcast(
                                        room_number,
                                        "3012 Game started. Please guess true or false",
                                    )
                                else:
                                    client.send("3011 Wait".encode())
                            else:
                                client.send("3013 The room is full".encode())
                    elif command.startswith("/guess"):
                        with self.rooms_lock:
                            # finding the room number the current client is in
                            room_number = [
                                key
                                for key, val in self.rooms.items()
                                # val is composed of (client, username)
                                # we are making another list with just clients (without username) to check if client is in it
                                if client in [i[0] for i in val]
                            ][0]
                        guess = command.split(" ")[1]
                        with self.guesses_lock:
                            self.guesses[room_number].append((client, guess))
                            if len(self.guesses[room_number]) == 2:
                                guess_values = [i[1] for i in self.guesses[room_number]]
                                if guess_values[0].lower() == guess_values[1].lower():
                                    self.broadcast(
                                        room_number, "3023 The result is a tie"
                                    )
                                else:
                                    bool_value = str(
                                        random.choice([True, False])
                                    ).lower()
                                    winner_client, loser_client = (
                                        (0, 1)
                                        if guess_values[0] == bool_value
                                        else (1, 0)
                                    )
                                    winner_client, loser_client = (
                                        self.guesses[room_number][winner_client][0],
                                        self.guesses[room_number][loser_client][0],
                                    )
                                    winner_client.send(
                                        "3021 You are the winner".encode()
                                    )
                                    loser_client.send(
                                        "3022 You lost this game".encode()
                                    )
                                self.guesses[room_number] = []
                                self.rooms[room_number] = []
                    elif command.startswith("/exit"):
                        client.send("4001 Bye bye".encode())
                        client.close()
                        with self.rooms_lock:
                            for room_number in self.rooms:
                                for player in self.rooms[room_number]:
                                    if player[0] == client:
                                        self.rooms[room_number].remove(player)
                                        break                                    
                        return
                    else:
                        client.send("4002 Unrecognized message".encode())

            else:
                client.send("1002 Authentication failed".encode())
        except:
            print("Client disconnected\n")
            client.close()
            with self.rooms_lock:
                for room_number in self.rooms:
                    for player in self.rooms[room_number]:
                        if player[0] == client:
                            self.rooms[room_number].remove(player)
                            break

    def start(self):
        while True:
            client, address = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


server = GameServer()
server.start()
