import sys
import threading

sys.path.append("../eqsn/")
from gates import new_qubit, cnot_gate, H_gate, X_gate, stop_all, measure

def test_non_destructive_measurement():
    id1 = str(1)
    new_qubit(id1)
    H_gate(id1)
    m = measure(id1, non_destructive=True)
    m2 = measure(id1)
    print("Measured %d." % m)
    assert m == m2
    print("Test was successfull!")
    stop_all()


test_non_destructive_measurement()
