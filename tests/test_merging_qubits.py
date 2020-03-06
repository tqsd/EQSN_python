from eqsn import new_qubit, stop_all
from eqsn.gates import merge_qubits


def test_merge():
    id1 = str(1)
    id2 = str(2)
    new_qubit(id1)
    new_qubit(id2)
    merge_qubits(id1, id2)
    stop_all()


if __name__ == "__main__":
    test_merge()
