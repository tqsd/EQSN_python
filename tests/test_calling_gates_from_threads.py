import threading
from eqsn import EQSN


def test_call_single_qubit_gate_from_threads():
    q_sim = EQSN()

    def call_X_gate_n_times(id, n):
        for c in range(n):
            # print("Apply %d time." % c)
            q_sim.X_gate(id)

    id1 = str(1)
    q_sim.new_qubit(id1)
    n = 999
    nr_threads = 5
    thread_list = []
    for _ in range(nr_threads):
        t = threading.Thread(target=call_X_gate_n_times, args=(id1, n))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    m = q_sim.measure(id1)
    assert m == 1
    q_sim.stop_all()


if __name__ == "__main__":
    test_call_single_qubit_gate_from_threads()
    exit(0)
