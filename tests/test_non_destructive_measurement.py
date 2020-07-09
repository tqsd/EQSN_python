from eqsn import EQSN


def test_non_destructive_measurement():
    q_sim = EQSN()
    id1 = str(1)
    q_sim.new_qubit(id1)
    q_sim.H_gate(id1)
    m = q_sim.measure(id1, non_destructive=True)
    m2 = q_sim.measure(id1)
    assert m == m2
    q_sim.stop_all()


if __name__ == "__main__":
    test_non_destructive_measurement()
    exit(0)
