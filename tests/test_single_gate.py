import sys
from eqsn import *


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


def test_S_gate():
    id = str(11)
    new_qubit(id)
    H_gate(id)
    S_gate(id)
    S_gate(id)
    H_gate(id)
    res = measure(id)
    print("measured %d." % res)
    assert res == 1
    stop_all()


def test_K_gate():
    print("test K gate.")
    id = str(11)
    new_qubit(id)
    H_gate(id)
    K_gate(id)
    K_gate(id)
    H_gate(id)
    res = measure(id)
    print("measured %d." % res)
    assert res == 0
    stop_all()


def test_measure():
    id = str(10)
    new_qubit(id)
    res = measure(id)
    assert res == 0
    stop_all()


if __name__=="__main__":
    test_x_gate()
    test_y_gate()
    test_z_gate()
    test_H_gate()
    test_T_gate()
    test_S_gate()
    test_K_gate()
    test_measure()
