import time

from eqsn import EQSN
import numpy as np


def test_two_qubit_gate():
    eqsn = EQSN()
    eqsn.new_qubit("100")
    eqsn.new_qubit("200")
    eqsn.X_gate("100")
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    )
    eqsn.custom_two_qubit_gate("100", "200", custom_gate)
    m1 = eqsn.measure("100")
    m2 = eqsn.measure("200")
    assert m1 == 0
    assert m2 == 1
    eqsn.stop_all()


def test_custom_two_qubit_control_gate_control_applied():
    eqsn = EQSN()
    eqsn.new_qubit("100")
    eqsn.new_qubit("200")
    eqsn.new_qubit("300")

    eqsn.X_gate("100")
    eqsn.X_gate("200")
    # Swap gate
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    )
    eqsn.custom_two_qubit_control_gate("100", "200", "300", custom_gate)

    m1 = eqsn.measure("100")
    m2 = eqsn.measure("200")
    m3 = eqsn.measure("300")

    assert m2 == 0
    assert m3 == 1
    assert m1 == 1

    eqsn.stop_all()


def test_custom_two_qubit_control_gate_control_not_applied():
    eqsn = EQSN()
    eqsn.new_qubit("100")
    eqsn.new_qubit("200")
    eqsn.new_qubit("300")
    eqsn.X_gate("200")
    # Swap gate
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    )
    eqsn.custom_two_qubit_control_gate("100", "200", "300", custom_gate)

    m1 = eqsn.measure("100")
    m2 = eqsn.measure("200")
    m3 = eqsn.measure("300")

    assert m2 == 1
    assert m3 == 0
    assert m1 == 0

    eqsn.stop_all()


def test_custom_two_qubit_control_gate_control_ccnot():
    eqsn = EQSN()
    eqsn.new_qubit("100")
    eqsn.new_qubit("200")
    eqsn.new_qubit("300")

    eqsn.X_gate("100")
    eqsn.X_gate("200")
    # Swap gate
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    eqsn.custom_two_qubit_control_gate("100", "200", "300", custom_gate)

    m1 = eqsn.measure("100")
    m2 = eqsn.measure("200")
    m3 = eqsn.measure("300")

    assert m2 == 1
    assert m3 == 1
    assert m1 == 1

    eqsn.stop_all()


def test_custom_two_qubit_control_gate_other_qubits_not_affected():
    eqsn = EQSN()

    eqsn.new_qubit("400")
    eqsn.new_qubit("200")
    eqsn.new_qubit("300")
    eqsn.new_qubit("100")
    eqsn.new_qubit("500")

    eqsn.X_gate("100")
    eqsn.X_gate("200")
    # Swap gate
    custom_gate = np.asarray(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    eqsn.custom_two_qubit_control_gate("100", "200", "300", custom_gate)

    m1 = eqsn.measure("100")
    m2 = eqsn.measure("200")
    m3 = eqsn.measure("300")
    m4 = eqsn.measure("400")
    m5 = eqsn.measure("500")

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
    exit(0)
