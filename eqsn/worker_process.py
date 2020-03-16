import logging
import threading
from eqsn.shared_dict import SharedDict
from eqsn.qubit_thread import SINGLE_GATE, MERGE_SEND, MERGE_ACCEPT, MEASURE,\
                MEASURE_NON_DESTRUCTIVE, GIVE_QUBITS_AND_TERMINATE, \
                CONTROLLED_GATE, QubitThread


class WorkerProcess(object):

    def __init__(self, queue):
        self.queue = queue
        self.shared_dict = SharedDict.get_instance()
        self.manager = threading.Manager()

    def run(self):
        pass

    def new_qubit(self, id):
        """
        Creates a new qubit with an id.

        Args:
            id (String): Id of the new qubit.
        """
        q = threading.Queue()
        thread = QubitThread(id, q)
        p = threading.Process(target=thread.run, args=())
        self.shared_dict.set_thread_with_id(id, p, q)
        p.start()
        logging.debug("Created new qubit with id %s.", id)

    def stop_all(self):
        """
        Stops the simulator from running.
        """
        self.shared_dict.send_all_threads(None)
        self.shared_dict.stop_all_threads()

    def apply_single_gate(self, gate, id):
        pass

    def apply_multi_gate(self, gate, id1, id2):
        """
        Applies a controlled gate, where the gate is applied to
        q_id1 and controlled by q_id2.

        Args:
            q_id1 (String): Id of the Qubit on which the X gate is applied.
            q_id2 (String): Id of the Qubit which controls the gate.
        """
        self.merge_qubits(id1, id2)
        q = self.shared_dict.get_queues_for_ids([id1])[0]
        q.put([CONTROLLED_GATE, gate, id1, id2])

    def merge_send(self, queue, id):
        pass

    def merge_pass(self, queue, id):
        pass

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
