import sys
import threading

sys.path.append("../src/")
from gates import new_qubit, cnot_gate, H_gate, X_gate, stop_all, measure

def test_call_single_qubit_gate_from_threads():
    def call_X_gate_n_times(id, n):
        for c in range(n):
            # print("Apply %d time." % c)
            X_gate(id)
    id1 = str(1)
    new_qubit(id1)
    n = 99
    nr_threads = 3
    thread_list = []
    for _ in range(nr_threads):
        t = threading.Thread(target=call_X_gate_n_times, args=(id1, n))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    m = measure(id1)
    print("Measured %d." % m)
    assert m == 1
    print("Test was successfull!")
    stop_all()


test_call_single_qubit_gate_from_threads()
