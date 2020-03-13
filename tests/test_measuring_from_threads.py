import threading
import random
import time

from eqsn import EQSN


def test_measure_from_threads():
    q_sim = EQSN()

    def measure_or_hadamard(id):
        n = random.randrange(10, 100, 1)
        for _ in range(n):
            time.sleep(0.1)
            q_sim.H_gate(id)
        print("Finished Hadamard, measure qubit %s!" % id)
        print(q_sim.measure(id))
        print("Finished with Measure!")

    nr_threads = 10
    ids = [str(x) for x in range(nr_threads)]
    for id in ids:
        q_sim.new_qubit(id)
    id1 = ids[0]
    for c in ids:
        if c != id1:
            q_sim.cnot_gate(id1, c)
    thread_list = []
    for id in ids:
        t = threading.Thread(target=measure_or_hadamard, args=(id))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print("Test was successfull!")
    q_sim.stop_all()


if __name__ == "__main__":
    test_measure_from_threads()
