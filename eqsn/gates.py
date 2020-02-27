import multiprocessing
from eqsn.qubit_thread import *
from eqsn.shared_dict import get_queues_for_ids, set_thread_with_id, \
    send_all_threads, stop_all_threads, \
    change_thread_and_queue_of_ids_and_join, delete_id_and_check_to_join_thread

manager = multiprocessing.Manager()


def new_qubit(id):
    """
    Creates a new qubit with an id.
    """
    q = multiprocessing.Queue()
    thread = QubitThread(id, q)
    p = multiprocessing.Process(target=thread.run, args=())
    set_thread_with_id(id, p, q)
    p.start()


def stop_all():
    """
    Stops the simulator from running.
    """
    send_all_threads(None)
    stop_all_threads()


def X_gate(q_id):
    """
    Applies the Pauli X gate to the Qubit with q_id.
    """
    x = np.array([[0, 1], [1, 0]], dtype=np.csingle)
    q = get_queues_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def Y_gate(q_id):
    """
    Applies the Pauli Y gate to the Qubit with q_id.
    """
    x = np.array([[0, 0 - 1j], [0 + 1j, 0]], dtype=np.csingle)
    q = get_queues_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def Z_gate(q_id):
    """
    Applies the Pauli Z gate to the Qubit with q_id.
    """
    x = np.array([[1, 0], [0, -1]], dtype=np.csingle)
    q = get_queues_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def H_gate(q_id):
    """
    Applies the Hadamard gate to the Qubit with q_id.
    """
    x = (1 / 2.0) ** 0.5 * np.array([[1, 1], [1, -1]], dtype=np.csingle)
    q = get_queues_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def T_gate(q_id):
    """
    Applies the T gate to the Qubit with q_id.
    """
    x = np.array([[1, 0], [0, (0.7071067811865476 + 0.7071067811865475j)]], dtype=np.csingle)
    q = get_queues_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def RX_gate(q_id, rad):
    """
    Applies the T gate to the Qubit with q_id.
    """
    mid = np.cos(rad / 2)
    other = -1j * np.sin(rad / 2)
    x = np.array([[mid, other], [other, mid]], dtype=np.csingle)
    q = get_queues_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def RY_gate(q_id, rad):
    """
    Applies the T gate to the Qubit with q_id.
    """
    mid = np.cos(rad / 2)
    other = np.sin(rad / 2)
    x = np.array([[mid, -1.0 * other], [other, mid]], dtype=np.csingle)
    q = get_queues_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def RZ_gate(q_id, rad):
    """
    Applies the T gate to the Qubit with q_id.
    """
    top = np.exp(-1j * (rad / 2))
    bot = np.exp(1j * (rad / 2))
    x = np.array([[top, 0], [0, bot]], dtype=np.csingle)
    q = get_queues_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def merge_qubits(q_id1, q_id2):
    """
    Merges two qubits to one process, if they are not already
    running in the same process.
    """
    l = get_queues_for_ids([q_id1, q_id2])
    if len(l) == 1:
        return  # Already merged
    else:
        # print("Merge qubits %s and %s" % (q_id1, q_id2))
        q1 = l[0]
        q2 = l[1]
        merge_q = manager.Queue()
        q1.put([MERGE_SEND, merge_q])
        q2.put([MERGE_ACCEPT, merge_q])
        qubits_q = manager.Queue()
        q1.put([GIVE_QUBITS_AND_TERMINATE, qubits_q])
        qubits = qubits_q.get()
        change_thread_and_queue_of_ids_and_join(qubits, q_id2)


def cnot_gate(q_id1, q_id2):
    """
    Applies a controlled X gate, where the gate is applied to
    q_id1 and controlled by q_id2.
    """
    x = np.array([[0, 1], [1, 0]], dtype=np.csingle)
    merge_qubits(q_id1, q_id2)
    q = get_queues_for_ids([q_id1])[0]
    q.put([CONTROLLED_GATE, x, q_id1, q_id2])


def cphase_gate(q_id1, q_id2):
    """
    Applies a controlled X gate, where the gate is applied to
    q_id1 and controlled by q_id2.
    """
    x = np.array([[0, 1], [0, -1]], dtype=np.csingle)
    merge_qubits(q_id1, q_id2)
    q = get_queues_for_ids([q_id1])[0]
    q.put([CONTROLLED_GATE, x, q_id1, q_id2])


def measure(id, non_destructive=False):
    """
    Measures a qubit with an id. If non_destructive is False, the qubit
    is removed from the system, otherwise, the qubit stays in the system after
    measurement, but its wavefunction collapses.
    """
    ret = manager.Queue()
    q = get_queues_for_ids([id])[0]
    if non_destructive:
        q.put([MEASURE_NON_DESTRUCTIVE, id, ret])
    else:
        q.put([MEASURE, id, ret])
    res = ret.get()
    if not non_destructive:
        delete_id_and_check_to_join_thread(id)
    return res
