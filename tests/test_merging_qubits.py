from eqsn import EQSN


def test_merge():
    q_sim = EQSN()
    id1 = str(1)
    id2 = str(2)
    q_sim.new_qubit(id1)
    q_sim.new_qubit(id2)
    q_sim.merge_qubits(id1, id2)
    q_sim.stop_all()


if __name__ == "__main__":
    test_merge()
