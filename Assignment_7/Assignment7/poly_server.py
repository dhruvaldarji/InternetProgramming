
import socket
import logging
import polynomials

__author__ = 'Dhruval'

"""
# DESCRIPTION ##########################################################################################################
The server will listen on port 12321.
It will carry out polynomial computations using the functions in the provided module.

Requests are in one of two formats:
    * Evaluate Request
        * Request starts with ‘E’
        * Followed by an argument value
        * Followed by a single space
        * Followed by he coefficients of a polynomial, separated by single spaces
        * Ex.) E1.0 -945 1689 -950 230 -25 1

    * Bisection Request
        * Requests starts with ‘S’
        * Followed by ‘a’, ‘b’, polynomial, tolerance separated by single spaces
########################################################################################################################
"""

logging.basicConfig(filename='poly_server.log', level=logging.INFO)

host = "localhost"
port = 12321

listener = socket.socket()   # listener is used just to start a connection
listener.bind((host, port))

listener.listen()
startMessage = "Server Started on {}:{}.\n".format(host, port)
print(startMessage)

while 1:
    conn = listener.accept()   # conn is used to communicate through a connection
    sock = conn[0]  # get the socket from the connection

    # get the request from the client
    request = ""
    encoded_message = sock.recv(2048)
    while len(encoded_message) > 0:
        request += encoded_message.decode()
        encoded_message = sock.recv(2048)  # possibility that decode error from

    # split encoding
    logging.info(" request received |" + request + "|")
    print("request received |" + request + "|")
    if len(request) == 0:
        message = "XEmpty request"
        logging.error(" response " + message)
        sock.sendall(message.encode())
        sock.shutdown(1)
    else:
        request_code = request[0]   # assuming the message has at least one character
        if request_code == "E":
            try:
                parameters = request[1:].split(' ')
                args = [float(x) for x in parameters]

                x = args[0]
                poly = args[1:]

                value = polynomials.evaluate(x, poly)

                message = "E" + str(value)
                logging.info("response " + message)
                sock.sendall(message.encode())
                sock.shutdown(1)
            except Exception as ex:
                logging.error("Input value conversion error " + request[1:])
                logging.error(str(ex))
                message = "X Invalid format numeric data: " + request[1:]
                logging.error("response " + message)
                sock.sendall(message.encode())
                sock.shutdown(1)

        elif request_code == "S":
            try:
                parameters = request[1:].split(' ')
                args = [float(x) for x in parameters]

                a = args[0]
                b = args[1]
                poly = args[2:8]
                tol = args[8]

                value = polynomials.bisection(a, b, poly, tol)

                message = "S" + str(value)
                logging.info("response " + message)
                sock.sendall(message.encode())
                sock.shutdown(1)
            except Exception as ex:
                logging.error("Input value conversion error " + request[1:])
                logging.error(str(ex))
                message = "X Invalid format numeric data: " + request[1:]
                logging.error("response " + message)
                sock.sendall(message.encode())
                sock.shutdown(1)

        else:
            message = "XInvalid request code: " + request_code
            logging.error("response " + message)
            sock.sendall(message.encode())
            sock.shutdown(1)

    sock.close()
