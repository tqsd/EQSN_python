import sys

sys.path.append("../eqsn/")
from gates import new_qubit, measure


if __name__ == "__main__":
    id = "Qubit"
    new_qubit(id)
    m = measure(id)
    print("Measured Qubit with result %d." % m)
