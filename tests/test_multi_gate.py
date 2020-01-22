import sys

sys.path.append("../src/")
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
    assert m1 == m2
    print("Test was successfull!")
    stop_all()

test_epr_creation()
