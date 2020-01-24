import sys

sys.path.append("../eqsn/")
from gates import *

def test_merge():
    id1 = str(1)
    id2 = str(2)
    new_qubit(id1)
    new_qubit(id2)
    merge_qubits(id1, id2)
    stop_all()

test_merge()
