import time

from eqsn import EQSN
import numpy as np


def test_two_qubit_gate():
    eqsn = EQSN()
    eqsn.new_qubit("1")
    eqsn.new_qubit("2")
    eqsn.X_gate("1")
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    )
    eqsn.custom_two_qubit_gate("1", "2", custom_gate)
    m1 = eqsn.measure("1")
    m2 = eqsn.measure("2")
    assert m1 == 0
    assert m2 == 1
    eqsn.stop_all()


def test_custom_two_qubit_control_gate_control_applied():
    eqsn = EQSN()
    eqsn.new_qubit("1")
    eqsn.new_qubit("2")
    eqsn.new_qubit("3")

    eqsn.X_gate("1")
    eqsn.X_gate("2")
    # Swap gate
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    )
    eqsn.custom_two_qubit_control_gate("1", "2", "3", custom_gate)

    m1 = eqsn.measure("1")
    m2 = eqsn.measure("2")
    m3 = eqsn.measure("3")

    assert m2 == 0
    assert m3 == 1
    assert m1 == 1

    eqsn.stop_all()


def test_custom_two_qubit_control_gate_control_not_applied():
    eqsn = EQSN()
    eqsn.new_qubit("1")
    eqsn.new_qubit("2")
    eqsn.new_qubit("3")
    eqsn.X_gate("2")
    # Swap gate
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    )
    eqsn.custom_two_qubit_control_gate("1", "2", "3", custom_gate)

    m1 = eqsn.measure("1")
    m2 = eqsn.measure("2")
    m3 = eqsn.measure("3")

    assert m2 == 1
    assert m3 == 0
    assert m1 == 0

    eqsn.stop_all()


def test_custom_two_qubit_control_gate_control_ccnot():
    eqsn = EQSN()
    eqsn.new_qubit("1")
    eqsn.new_qubit("2")
    eqsn.new_qubit("3")

    eqsn.X_gate("1")
    eqsn.X_gate("2")
    # Swap gate
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    eqsn.custom_two_qubit_control_gate("1", "2", "3", custom_gate)

    m1 = eqsn.measure("1")
    m2 = eqsn.measure("2")
    m3 = eqsn.measure("3")

    assert m2 == 1
    assert m3 == 1
    assert m1 == 1

    eqsn.stop_all()


def test_custom_two_qubit_control_gate_other_qubits_not_affected():
    eqsn = EQSN()
    eqsn.new_qubit("4")
    eqsn.new_qubit("2")
    eqsn.new_qubit("3")
    eqsn.new_qubit("1")
    eqsn.new_qubit("5")

    eqsn.X_gate("1")
    eqsn.X_gate("2")
    # Swap gate
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    eqsn.custom_two_qubit_control_gate("1", "2", "3", custom_gate)

    m1 = eqsn.measure("1")
    m2 = eqsn.measure("2")
    m3 = eqsn.measure("3")
    m4 = eqsn.measure("4")
    m5 = eqsn.measure("5")

    assert m2 == 1
    assert m3 == 1
    assert m1 == 1
    assert m4 == 0
    assert m5 == 0

    eqsn.stop_all()


if __name__ == "__main__":
    test_list = [test_two_qubit_gate,
                 test_custom_two_qubit_control_gate_control_applied,
                 test_custom_two_qubit_control_gate_control_not_applied,
                 test_custom_two_qubit_control_gate_control_ccnot,
                 test_custom_two_qubit_control_gate_other_qubits_not_affected]
    for func in test_list:
        func()
        time.sleep(0.5)
