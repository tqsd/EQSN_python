from eqsn import EQSN
import numpy as np

def test_custom_single_gate():
    eqsn = EQSN()
    gate = (1/2)**0.5 * np.array([[1, 1],[1,-1]], dtype=np.csingle)
    eqsn.new_qubit('1')
    eqsn.custom_gate('1', gate)
    eqsn.custom_gate('1', gate)
    res = eqsn.measure('1')
    eqsn.stop_all()
    assert res == 0

def test_custom_controlled_gate():
    eqsn = EQSN()
    gate = np.array([[0, 1],[1,0]], dtype=np.csingle)
    eqsn.new_qubit('1')
    eqsn.new_qubit('2')
    eqsn.H_gate('1')
    eqsn.custom_controlled_gate('2', '1', gate)
    res1 = eqsn.measure('1')
    res2 = eqsn.measure('2')
    eqsn.stop_all()
    assert res1 == res2


if __name__ == "__main__":
    print("Start custom gate tests...")
    test_custom_single_gate()
    test_custom_controlled_gate()
    print("Finished custom gates test.")
