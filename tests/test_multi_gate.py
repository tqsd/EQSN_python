from eqsn import EQSN
import time


def test_epr_creation():
    q_sim = EQSN()
    id1 = str(1)
    id2 = str(2)
    q_sim.new_qubit(id1)
    q_sim.new_qubit(id2)
    q_sim.H_gate(id2)
    q_sim.cnot_gate(id1, id2)
    m1 = q_sim.measure(id1)
    m2 = q_sim.measure(id2)
    print("measured %d and %d." % (m1, m2))
    assert m1 == m2
    print("Test was successfull!")
    q_sim.stop_all()


def test_5_qubits_gate():
    q_sim = EQSN()
    ids = [str(x) for x in range(5)]
    for i in ids:
        q_sim.new_qubit(i)
    for i in ids:
        q_sim.H_gate(i)
    q_sim.cnot_gate(ids[1], ids[0])
    q_sim.cnot_gate(ids[2], ids[1])
    q_sim.cnot_gate(ids[3], ids[2])
    q_sim.cnot_gate(ids[4], ids[3])
    for i in ids:
        m = q_sim.measure(i)
        print("Qubit %s was %d." % (i, m))
    q_sim.stop_all()


if __name__ == "__main__":
    test_epr_creation()
    time.sleep(0.1)
    test_5_qubits_gate()
