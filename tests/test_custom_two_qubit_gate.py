from eqsn import EQSN
import time
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


if __name__ == "__main__":
    test_two_qubit_gate()
