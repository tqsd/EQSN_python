import sys
import threading
import random
import time

from eqsn import *

def test_measure_from_threads():
    def measure_or_hadamard(id):
        n = random.randrange(10,100,1)
        for _ in range(n):
            time.sleep(0.1)
            H_gate(id)
        print("Finished Hadamard, measure qubit %s!" % id)
        print(measure(id))
        print("Finished with Measure!")
    nr_threads = 10
    ids = [str(x) for x in range(nr_threads)]
    for id in ids:
        new_qubit(id)
    id1 = ids[0]
    for c in ids:
        if c != id1:
            cnot_gate(id1, c)
    thread_list = []
    for id in ids:
        t = threading.Thread(target=measure_or_hadamard, args=(id))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print("Test was successfull!")
    stop_all()


test_measure_from_threads()
