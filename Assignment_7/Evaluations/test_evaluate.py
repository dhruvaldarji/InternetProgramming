from polynomials import evaluate, bisection

# Evaluate
print("=========== Evaluate ===========")

message = "E1.0 -945 1689 -950 230 -25 1"

argsStr = message[1:].split(' ')
args = [float(x) for x in argsStr]

x = args[0]
poly = args[1:]
result = evaluate(x, poly)
print("Evaluation: " + str(result))
print("===============================\n")

# Bisection
print("========== Bisection ==========")

message = "S0 2 -945 1689 -950 230 -25 1 1e-15"

argsStr = message[1:].split(' ')
args = [float(x) for x in argsStr]

a = args[0]
b = args[1]
poly = args[2:8]
tol = args[8]

print('a: ' + str(a))
print('b: ' + str(b))
print('poly: ' + str(poly))
print('tol: ' + str(tol))

result = bisection(a, b, poly, tol)
print("Bisection: " + str(result))
print("===============================")

