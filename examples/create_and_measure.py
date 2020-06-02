from eqsn import EQSN


if __name__ == "__main__":
    eqsn = EQSN()
    id = "Qubit"
    eqsn.new_qubit(id)
    m = eqsn.measure(id)
    print("Measured Qubit with result %d." % m)
