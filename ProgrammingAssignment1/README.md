# GameServer and GameClient Documentation

This README outlines the functionalities of a simple game server and client implemented using Python's socket and threading libraries.

## GameServer

The GameServer is the main game host which manages multiple game rooms and user sessions. The server is initialized on a specific host and port, and it listens for incoming client connections.

### Key Features:
1. **User Authentication**: The server reads from a file named "UserInfo.txt" and stores the usernames and passwords. When a client attempts to connect, it asks for these credentials and validates them. The server sends a response indicating whether the authentication was successful or not.

2. **Game Rooms Management**: The server manages multiple game rooms. It keeps track of the clients present in each room and their guesses. The rooms and guesses are protected with locks to prevent race conditions.

3. **Command Handling**: The server handles various commands from the clients such as `/list`, `/enter`, `/guess`, and `/exit`. 

4. **Game Logic**: The server also implements the game logic. When two clients have joined a room and made their guesses, it determines the winner and sends appropriate messages to the clients.

## GameClient

The GameClient is the player's interface to interact with the GameServer. Each client connects to the server and communicates with it using various commands.

### Key Features:
1. **User Authentication**: The client sends username and password for authentication to the server upon connection.

2. **Command Sending**: The client continuously reads user input from the command line and sends it to the server. It can send commands like `/list`, `/enter`, `/guess`, and `/exit`.

3. **Response Handling**: The client handles responses from the server and prints them out to the console. If the server sends a "4001 Bye bye" response or if the connection to the server is lost, the client exits.

## How to Run:

1. Start the server by running `python3 GameServer.py`. The server will start listening for incoming connections.

2. Start the client by running `python3 GameClient.py` . The client will connect to the server and ask for username and password.

3. After successful authentication, you can enter commands to interact with the server.

## Commands:

- `/list`: Lists the current number of players in each game room.
- `/enter [room_number]`: Joins the specified game room.
- `/guess [true/false]`: Makes a guess in the current game room.
- `/exit`: Exits the client.
- Any other inputs will throw a `4002 Unrecognized message`

## Note:

This project is a simple demonstration of a multi-threaded game server and does not include complex game logic or robust error handling. It's advised to handle exceptions and edge cases in a production-level project.