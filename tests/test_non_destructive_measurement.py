from eqsn import new_qubit, H_gate, measure, stop_all


def test_non_destructive_measurement():
    id1 = str(1)
    new_qubit(id1)
    H_gate(id1)
    m = measure(id1, non_destructive=True)
    m2 = measure(id1)
    print("Measured %d." % m)
    assert m == m2
    print("Test was successfull!")
    stop_all()


if __name__ == "__main__":
    test_non_destructive_measurement()
