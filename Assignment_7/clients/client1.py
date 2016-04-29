

import socket

sck = socket.socket()
sck.connect(("localhost", 12321))

# Evaluate
message = "E1.0 -945 1689 -950 230 -25 1"
encoded_message = message.encode()
sck.sendall(encoded_message)
sck.shutdown(1)

response = ""
encoded_message = sck.recv(2048)
while len(encoded_message) > 0:
    response += encoded_message.decode()
    encoded_message = sck.recv(2048)

print("received: " + response)


sck.close()
