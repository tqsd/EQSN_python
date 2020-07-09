import threading
import random
import time

from eqsn import EQSN


def test_measure_from_threads():
    q_sim = EQSN()

    def measure_or_hadamard(_id):
        n = random.randrange(10, 100, 1)
        for _ in range(n):
            time.sleep(0.05)
            q_sim.H_gate(_id)

    nr_threads = 10
    ids = [str(x) for x in range(nr_threads)]
    for _id in ids:
        q_sim.new_qubit(_id)
    id1 = ids[0]
    for c in ids:
        if c != id1:
            q_sim.cnot_gate(id1, c)
    thread_list = []
    for _id in ids:
        t = threading.Thread(target=measure_or_hadamard, args=(_id,))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    q_sim.stop_all()


if __name__ == "__main__":
    test_measure_from_threads()
    exit(0)
