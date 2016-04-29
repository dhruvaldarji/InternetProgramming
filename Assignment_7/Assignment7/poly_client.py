import socket

__author__ = 'Dhruval'

'''
# DESCRIPTION ##########################################################################################################
# This Client connects to a Polynomial Server at "localhost:12321",
# Evaluates a Bisection,
# And then Evaluates a polynomial based on the result.

# Bisection :   S0 2 -945 1689 -950 230 -25 1 1e-15
# Evaluate  :   E1.0 -945 1689 -950 230 -25 1
########################################################################################################################
'''

host = "localhost"
port = 12321


# Evaluate which mode we are based on code and construct the proper message string.
def eval_mode(_c, _a, _b, _p, _t):
    if _c == "E":
        msg = _c + str(_a) + " "
        msg += ' '.join(str(x) for x in _p)
    elif code == "S":
        msg = _c + str(_a) + " " + str(_b) + " "
        msg += ' '.join(str(x) for x in _p)
        msg += " " + str(_t)
    else:  # Default, just add all parameters and keep going. Server should catch any errors.
        msg = _c + str(_a) + " " + str(_b) + " "
        msg += ' '.join(str(x) for x in _p)
        msg += " " + str(_t)
    return msg


# Send a message to the server with the given variables.
def send(_c, _a, _b, _p, _t):
    sck = socket.socket()
    sck.connect((host, port))
    
    message = eval_mode(_c, _a, _b, _p, _t)
    print("Sending: " + message)
    encoded_message = message.encode()
    sck.sendall(encoded_message)
    sck.shutdown(1)

    res = ""
    encoded_message = sck.recv(2048)
    while len(encoded_message) > 0:
        res += encoded_message.decode()
        encoded_message = sck.recv(2048)

    print("Received: " + res)
    print()

    sck.close()
    return res

# __main __ ############################################################################################################

# VARIABLES
code = "S"
a = 0
b = 2
poly = [-945, 1689, -950, 230, -25, 1]
tol = 1e-15

print()

response = send(code, a, b, poly, tol)
resCode = response[0]

if resCode == "E":
    # do nothing
    pass
elif resCode == "S":
    a = float(response[1:])
    code = "E"
    send(code, a, b, poly, tol)
