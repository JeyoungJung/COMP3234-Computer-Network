import threading, socket, sys


class GameClient:
    def __init__(self, host="localhost", port=4003):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send_command(self):
        while True:
            command = input()
            self.client.send(command.encode())
            if command.startswith("/exit"):
                sys.exit()

    def receive_response(self):
        while True:
            try:
                response = self.client.recv(1024).decode()
                if not response:  # Server connection lost
                    print("Server connection lost")
                    sys.exit()

                if response == "4001 Bye bye":
                    print("Client ends")
                    sys.exit()

                print(f"{response}")

            except socket.error:  # Handle socket errors (like a broken connection)
                print("Server connection lost")
                sys.exit()

    def start(self):
        send_thread = threading.Thread(target=self.send_command)
        receive_thread = threading.Thread(target=self.receive_response)
        send_thread.start()
        receive_thread.start()


client = GameClient()
client.start()
