import multiprocessing
import numpy as np
from qubit_thread import QubitThread, SINGLE_GATE, DOUBLE_GATE, MEASURE
from shared_dict import get_threads_for_ids, set_thread_with_id, \
                        send_all_threads, stop_all_threads

manager = multiprocessing.Manager()
def new_qubit(id):
    q = multiprocessing.Queue()
    thread = QubitThread(id, q)
    p = multiprocessing.Process(target=thread.run, args=())
    set_thread_with_id(id, p, q)
    p.start()

def stop_all():
    send_all_threads(None)
    stop_all_threads()

def X_gate(q_id):
    x = np.array([[0,1],[1,0]], dtype=np.csingle)
    q = get_threads_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])

def Y_gate(q_id):
    x = np.array([[0,0-1j],[0+1j,0]], dtype=np.csingle)
    q = get_threads_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])

def Z_gate(q_id):
    x = np.array([[1,0],[0,-1]], dtype=np.csingle)
    q = get_threads_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])

def H_gate(q_id):
    x = np.array([[0.5,0.5],[0.5,-0.5]], dtype=np.csingle)
    q = get_threads_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])

def cnot_gate(id1, id2):
    pass


def measure(id):
    ret = manager.Queue()
    q = get_threads_for_ids([id])[0]
    q.put([MEASURE, id, ret])
    res = ret.get()
    return res
