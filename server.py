import socket
import threading

# Store all active connections and client information
# ----------------------------------------------R--
# List to store all connected client sockets
clients = []          

# Dictionary to map client sockets to their IP addresses
addresses = {}        

# Dictionary to map client sockets to their chosen nicknames
users = {}           

def broadcast(message, sender_socket=None):
    # Function to send a message to all connected clients except the sender
    # Args:
    #   message: The message to broadcast
    #   sender_socket: The socket of the client sending the message (to exclude them)
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode("utf8"))
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                remove_client(client)

def remove_client(client):
    # Safely remove a client and close their connection
    # Args:
    #   client: The socket connection to remove
    if client in clients:
        clients.remove(client)
        client.close()

def client_thread(client):
    # Handle the entire lifecycle of a client connection
    # Args:
    #   client: The socket connection for this client
    
    # Get client's IP address
    address = addresses[client][0]
    
    # Initial client setup - Get their chosen nickname
    try:
        client.send("Enter your nickname: ".encode("utf8"))
        while True:
            nickname = client.recv(2048).decode("utf8").strip()
            if not nickname:
                client.send("Nickname cannot be empty. Please enter a valid nickname: ".encode("utf8"))
            elif nickname in users.values():
                client.send("This nickname is already taken. Please choose another: ".encode("utf8"))
            else:
                users[client] = nickname
                break
    except Exception as e:
        print(f"Error setting nickname for {address}: {e}")
        remove_client(client)
        return

    # Announce new client connection
    print(f"{address} connected as {nickname}")
    broadcast(f"{nickname} has joined the chat!", None)

    # Main message handling loop
    while True:
        try:
            # Receive and process client messages
            message = client.recv(2048).decode("utf8").strip()
            
            # Handle private messages (/pm command)
            if message.startswith("/pm "):
                parts = message.split(" ", 2)
                if len(parts) > 2:
                    recipient = parts[1]
                    private_message = parts[2]
                    
                    # Find the recipient's socket
                    recipient_socket = None
                    for client_socket, client_nickname in users.items():
                        if client_nickname == recipient:
                            recipient_socket = client_socket
                            break
                    
                    # Send private message if recipient found
                    if recipient_socket:
                        recipient_socket.send(f"[Private from {nickname}]: {private_message}".encode("utf8"))
                        client.send(f"Private message sent to {recipient}: {private_message}".encode("utf8"))
                    else:
                        client.send(f"Error: User {recipient} not found.".encode("utf8"))
                else:
                    client.send("Error: Invalid private message format. Use /pm <user> <message>".encode("utf8"))
            
            # Handle client disconnection (/quit command)
            elif message == "/quit":
                broadcast(f"{nickname} has left the chat.", None)
                remove_client(client)
                del addresses[client]
                del users[client]
                print(f"{address} ({nickname}) disconnected.")
                break
            
            # Show online users (/online command)
            elif message == "/online":
                online_users = ', '.join(users.values())
                client.send(f"Users online: {online_users}".encode("utf8"))
            
            # Display help message (/help command)
            elif message == "/help":
                help_message = (
                    "Commands:\n"
                    "/quit - Leave the chat\n"
                    "/online - List online users\n"
                    "/help - Show this message"
                )
                client.send(help_message.encode("utf8"))
            
            # Handle typing notification (/typing command)
            elif message == "/typing":
                broadcast(f"[Typing]: {nickname} is typing...", client)
            
            # Handle regular chat messages
            else:
                print(f"{nickname} ({address}): {message}")
                broadcast(f"{nickname}: {message}", client)
                
        except Exception as e:
            # Handle unexpected client disconnection or errors
            print(f"Error handling client {address} ({nickname}): {e}")
            remove_client(client)
            broadcast(f"{nickname} has left the chat.", None)
            del addresses[client]
            del users[client]
            break

def start_server():
    # Initialize and start the chat server
    # Sets up socket connection and handles new client connections
    
    # Server configuration
    server_host = "localhost"
    server_port = 25000

    # Create and configure server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    # Allow up to 5 queued connections
    server_socket.listen(5)  
    print(f"Server started on {server_host}:{server_port}")

    # Main server loop
    while True:
        # Accept new client connections
        client, addr = server_socket.accept()
        print(f"New connection from {addr}")
        
        # Store client information
        clients.append(client)
        addresses[client] = addr

        # Create new thread to handle this client
        threading.Thread(target=client_thread, args=(client,), daemon=True).start()

if __name__ == "__main__":
    try:
        # Start the server
        start_server()
    except KeyboardInterrupt:
        # Handle clean server shutdown
        print("Server shutting down...")
