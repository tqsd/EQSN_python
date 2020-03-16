import multiprocessing
import logging
import numpy as np
from eqsn.qubit_thread import SINGLE_GATE, MERGE_SEND, MERGE_ACCEPT, MEASURE,\
                MEASURE_NON_DESTRUCTIVE, GIVE_QUBITS_AND_TERMINATE, \
                CONTROLLED_GATE, QubitThread
from eqsn.shared_dict import SharedDict


class EQSN(object):
    """
    Main object of EQSN, with this object, all of the Qubits can be controlled.
    All functions are threadsafe, but at the moment, only one instance should be
    used.
    """

    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.shared_dict = SharedDict.get_instance()

    def new_qubit(self, id):
        """
        Creates a new qubit with an id.

        Args:
            id (String): Id of the new qubit.
        """
        q = multiprocessing.Queue()
        thread = QubitThread(id, q)
        p = multiprocessing.Process(target=thread.run, args=())
        self.shared_dict.set_thread_with_id(id, p, q)
        p.start()
        logging.debug("Created new qubit with id %s.", id)

    def stop_all(self):
        """
        Stops the simulator from running.
        """
        self.shared_dict.send_all_threads(None)
        self.shared_dict.stop_all_threads()

    def X_gate(self, q_id):
        """
        Applies the Pauli X gate to the Qubit with q_id.
        """
        x = np.array([[0, 1], [1, 0]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def Y_gate(self, q_id):
        """
        Applies the Pauli Y gate to the Qubit with q_id.
        """
        x = np.array([[0, 0 - 1j], [0 + 1j, 0]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def Z_gate(self, q_id):
        """
        Applies the Pauli Z gate to the Qubit with q_id.
        """
        x = np.array([[1, 0], [0, -1]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def H_gate(self, q_id):
        """
        Applies the Hadamard gate to the Qubit with q_id.
        """
        x = (1 / 2.0) ** 0.5 * np.array([[1, 1], [1, -1]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def T_gate(self, q_id):
        """
        Applies the T gate to the Qubit with q_id.
        """
        x = np.array(
            [[1, 0], [0, (0.7071067811865476 + 0.7071067811865475j)]],
            dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def S_gate(self, q_id):
        """
        Applies the S gate to the Qubit with q_id.
        """
        x = np.array([[1, 0], [0, 1j]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def K_gate(self, q_id):
        """
        Applies the K gate to the Qubit with q_id.
        """
        x = 0.5 * np.array([[1+1j, 1-1j], [-1+1j, -1-1j]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def RX_gate(self, q_id, rad):
        """
        Applies the T gate to the Qubit with q_id.
        """
        mid = np.cos(rad / 2)
        other = -1j * np.sin(rad / 2)
        x = np.array([[mid, other], [other, mid]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def RY_gate(self, q_id, rad):
        """
        Applies the T gate to the Qubit with q_id.
        """
        mid = np.cos(rad / 2)
        other = np.sin(rad / 2)
        x = np.array([[mid, -1.0 * other], [other, mid]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def RZ_gate(self, q_id, rad):
        """
        Applies the T gate to the Qubit with q_id.
        """
        top = np.exp(-1j * (rad / 2))
        bot = np.exp(1j * (rad / 2))
        x = np.array([[top, 0], [0, bot]], dtype=np.csingle)
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, x, q_id])

    def merge_qubits(self, q_id1, q_id2):
        """
        Merges two qubits to one process, if they are not already
        running in the same process.

        Args:
            q_id1 (String): Id of the Qubit merged into q_id2.
            q_id2 (String): Id of the Qubit merged with q_id1.
        """
        l = self.shared_dict.get_queues_for_ids([q_id1, q_id2])
        if len(l) == 1:
            return  # Already merged
        else:
            logging.debug("Merge Qubits %s and %s.", q_id1, q_id2)
            q1 = l[0]
            q2 = l[1]
            merge_q = self.manager.Queue()
            q1.put([MERGE_SEND, merge_q])
            q2.put([MERGE_ACCEPT, merge_q])
            qubits_q = self.manager.Queue()
            q1.put([GIVE_QUBITS_AND_TERMINATE, qubits_q])
            qubits = qubits_q.get()
            self.shared_dict.change_thread_and_queue_of_ids_and_join(
                qubits, q_id2)

    def cnot_gate(self, q_id1, q_id2):
        """
        Applies a controlled X gate, where the gate is applied to
        q_id1 and controlled by q_id2.

        Args:
            q_id1 (String): Id of the Qubit on which the X gate is applied.
            q_id2 (String): Id of the Qubit which controls the gate.
        """
        x = np.array([[0, 1], [1, 0]], dtype=np.csingle)
        self.merge_qubits(q_id1, q_id2)
        q = self.shared_dict.get_queues_for_ids([q_id1])[0]
        q.put([CONTROLLED_GATE, x, q_id1, q_id2])

    def cphase_gate(self, q_id1, q_id2):
        """
        Applies a controlled Z gate, where the gate is applied to
        q_id1 and controlled by q_id2.
        """
        x = np.array([[0, 1], [0, -1]], dtype=np.csingle)
        self.merge_qubits(q_id1, q_id2)
        q = self.shared_dict.get_queues_for_ids([q_id1])[0]
        q.put([CONTROLLED_GATE, x, q_id1, q_id2])

    def measure(self, id, non_destructive=False):
        """
        Measures a qubit with an id. If non_destructive is False, the qubit
        is removed from the system, otherwise, the qubit stays in the system
        after measurement, but its wavefunction collapses.

        Args:
            id (String): Id of the Qubit which should be measured.
            non_destructive(bool): If a qubit should not be removed from the
                                    system after measurement.
        """
        ret = self.manager.Queue()
        q = self.shared_dict.get_queues_for_ids([id])[0]
        if non_destructive:
            q.put([MEASURE_NON_DESTRUCTIVE, id, ret])
        else:
            q.put([MEASURE, id, ret])
        res = ret.get()
        if not non_destructive:
            self.shared_dict.delete_id_and_check_to_join_thread(id)
        logging.debug(
            "Qubit with id %s has been measured with outcome %d.", id, res)
        return res
