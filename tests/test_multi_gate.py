import sys

sys.path.append("../eqsn/")
from gates import new_qubit, cnot_gate, H_gate, stop_all, measure


def test_epr_creation():
    id1 = str(1)
    id2 = str(2)
    new_qubit(id1)
    new_qubit(id2)
    H_gate(id2)
    cnot_gate(id1, id2)
    m1 = measure(id1)
    m2 = measure(id2)
    print("measured %d and %d." % (m1, m2))
    assert m1 == m2
    print("Test was successfull!")
    stop_all()


def test_5_qubits_gate():
    ids = [str(x) for x in range(5)]
    for i in ids:
        new_qubit(i)
    for i in ids:
        H_gate(i)
    cnot_gate(ids[1], ids[0])
    cnot_gate(ids[2], ids[1])
    cnot_gate(ids[3], ids[2])
    cnot_gate(ids[4], ids[3])
    for i in ids:
        m = measure(i)
        print("Qubit %s was %d." % (i, m))
    stop_all()


test_epr_creation()
test_5_qubits_gate()
