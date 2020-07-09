import threading
from eqsn import EQSN


def test_call_single_qubit_gate_from_threads():
    eqsn = EQSN()

    def call_X_gate_n_times(_id, n):
        for _ in range(n):
            eqsn.X_gate(_id)

    id1 = str(1)
    eqsn.new_qubit(id1)
    n = 99
    nr_threads = 5
    thread_list = []
    for _ in range(nr_threads):
        t = threading.Thread(target=call_X_gate_n_times, args=(id1, n))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    m = eqsn.measure(id1)
    assert m == 1
    eqsn.stop_all()


if __name__ == "__main__":
    test_call_single_qubit_gate_from_threads()
    exit(0)
