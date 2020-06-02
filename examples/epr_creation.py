from eqsn import EQSN


if __name__ == "__main__":
    eqsn = EQSN()
    eqsn.new_qubit('A')
    eqsn.new_qubit('B')
    eqsn.H_gate('A')
    eqsn.cnot_gate('B', 'A')
    m1 = eqsn.measure('A')
    m2 = eqsn.measure('B')
    print("Measured entangled pair with results %d and %d." % (m1, m2))
