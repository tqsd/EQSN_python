import sys

sys.path.append("../eqsn/")
from gates import *

def test_x_gate():
    id = str(10)
    new_qubit(id)
    X_gate(id)
    res = measure(id)
    assert res == 1
    stop_all()

def test_y_gate():
    id = str(10)
    new_qubit(id)
    Y_gate(id)
    Y_gate(id)
    res = measure(id)
    assert res == 0
    stop_all()

def test_z_gate():
    id = str(10)
    new_qubit(id)
    Z_gate(id)
    Z_gate(id)
    res = measure(id)
    assert res == 0
    stop_all()

def test_H_gate():
    id = str(10)
    new_qubit(id)
    H_gate(id)
    H_gate(id)
    res = measure(id)
    assert res == 0
    stop_all()

def test_T_gate():
    id = str(10)
    new_qubit(id)
    T_gate(id)
    res = measure(id)
    print("measured %d." % res)
    assert res == 0
    id = str(11)
    new_qubit(id)
    H_gate(id)
    T_gate(id)
    T_gate(id)
    T_gate(id)
    T_gate(id)
    H_gate(id)
    res = measure(id)
    print("measured %d." % res)
    assert res == 1
    stop_all()

def test_measure():
    id = str(10)
    new_qubit(id)
    res = measure(id)
    assert res == 0
    stop_all()


test_x_gate()
test_y_gate()
test_z_gate()
test_H_gate()
test_T_gate()
test_measure()
