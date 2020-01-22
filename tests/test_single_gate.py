import sys

sys.path.append("../src/")
from gates import new_qubit, X_gate, Y_gate, stop_all, measure

def test_x_gate():
    id = str(10)
    new_qubit(id)
    X_gate(id)
    stop_all()

def test_measure():
    id = str(10)
    new_qubit(id)
    res = measure(id)
    assert res == 0
    stop_all()


test_x_gate()
test_measure()
