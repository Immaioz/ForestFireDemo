import socket
import threading
from flask import Flask, jsonify, render_template
from message_pb2 import Messaggio  

app = Flask(__name__)

received_messages = []  # List to store the received messages
lock = threading.Lock()  # Lock for thread synchronization
index = 0
@app.route('/')
def index():
    global received_messages
    messages = []
    for message in received_messages:
        if message:
            message_dict = {
                'id': message.id,
                'data': message.data
            }
        else:
            message_dict = {
                'id': "not connected",
                'data': 0
            }
        messages.append(message_dict)
    return jsonify(messages=messages)

@app.route('/view')
def view():
    global received_messages
    messages = []
    for message in received_messages:
        if message:
            message_dict = {
                'id': message.id,
                'data': message.data
            }
        else:
            message_dict = {
                'id': "not connected",
                'data': 0
            }
        messages.append(message_dict)
    return render_template('index.html', messages=messages)

@app.route('/message/<int:index>')
def get_message(index):
    global received_messages
    if index >= 0 and index < len(received_messages):
        message = received_messages[index]
        if message:
            # Create a dictionary with the message content
            message_dict = {
                'id': message.id,
                'data': message.data
            }
            return jsonify(message_dict)
    return jsonify({})

def handle_client(conn, index):
    global received_messages
    try:
        # Receive the message
        serialized_message = conn.recv(1024)

        # Parse the serialized message
        message = Messaggio()
        message.ParseFromString(serialized_message)

        # Store the received message
        # print("index =", index)
        print("Received message:")
        print("ID:", message.id)
        print("Data:", message.data)
        new_index = message.id - 1

        
        with lock:
            received_messages[new_index]=message

        print("Received message from client", index)

    except Exception as e:
        print("Error handling client", index, ":", str(e))

    finally:
        # Close the connection
        conn.close()
        print("Connection with client", index, "closed.")

def receive_messages(host, port):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to a specific host and port
        sock.bind((host, port))

        # Listen for incoming connections
        sock.listen(3)
        print("Waiting for connections...")

        while True:
            # Accept a connection
            conn, addr = sock.accept()
            print("Connected to:", addr)
            

            index = addr[1]

            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(conn, index))
            client_thread.start()

    except KeyboardInterrupt:
        print("Receiver stopped.")
    finally:
        # Close the socket
        sock.close()

# Specify the host and port to listen on
host = 'localhost'
port = 1234

for i in range(3):
    received_messages.insert(i, None)

# Start the receiver in a separate thread
receiver_thread = threading.Thread(target=receive_messages, args=(host, port))
receiver_thread.start()

# Run the Flask web application
app.run()
