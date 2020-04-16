import logging
import threading
import os
from queue import Queue
from eqsn.shared_dict import SharedDict
from eqsn.qubit_thread import SINGLE_GATE, MERGE_SEND, MERGE_ACCEPT, MEASURE,\
                MEASURE_NON_DESTRUCTIVE, GIVE_STATEVECTOR, \
                CONTROLLED_GATE, NEW_QUBIT, ADD_MERGED_QUBITS_TO_DICT, \
                DOUBLE_GATE, QubitThread


class WorkerProcess(object):

    def __init__(self, queue):
        self.queue = queue
        # Get a new instance, since their might be one from the old process
        self.shared_dict = SharedDict.get_new_instance()

    def run(self):
        """
        Run in loop and wait to receive tasks to perform.
        """
        amount_single_gate = 0
        while True:
            item = self.queue.get()
            if item is None:
                self.stop_all()
                return
            elif item[0] == NEW_QUBIT:
                self.new_qubit(item[1])
            elif item[0] == SINGLE_GATE:
                self.apply_single_gate(item[1], item[2])
                amount_single_gate += 1
            elif item[0] == CONTROLLED_GATE:
                self.apply_controlled_gate(item[1], item[2], item[3])
            elif item[0] == MEASURE:
                self.measure(item[1], item[2])
            elif item[0] == MERGE_ACCEPT:
                self.merge_accept(item[1], item[2])
            elif item[0] == MERGE_SEND:
                self.merge_send(item[1], item[2], item[3])
            elif item[0] == MEASURE_NON_DESTRUCTIVE:
                self.measure_non_destructive(item[1], item[2])
            elif item[0] == ADD_MERGED_QUBITS_TO_DICT:
                self.add_merged_qubits_to_thread(item[1], item[2])
            elif item[0] == GIVE_STATEVECTOR:
                self.give_statevector_for(item[1], item[2])
            elif item[0] == DOUBLE_GATE:
                self.apply_two_qubit_gate(item[1], item[2], item[3])
            else:
                raise ValueError("Command does not exist!")

    def new_qubit(self, q_id):
        """
        Creates a new qubit with an id.

        Args:
            id (String): Id of the new qubit.
        """
        q = Queue()
        thread = QubitThread(q_id, q)
        p = threading.Thread(target=thread.run, args=())
        self.shared_dict.set_thread_with_id(q_id, p, q)
        p.start()
        logging.debug("Created new qubit with id %s.", q_id)

    def measure(self, q_id, channel):
        temp_queue = Queue()
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([MEASURE, q_id, temp_queue])
        res = temp_queue.get()
        channel.put(res)
        self.shared_dict.delete_id_and_check_to_join_thread(q_id)

    def measure_non_destructive(self, q_id, channel):
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([MEASURE_NON_DESTRUCTIVE, q_id, channel])

    def add_merged_qubits_to_thread(self, q_id, qubits):
        q, t = self.shared_dict.get_queues_and_threads_for_ids([q_id])[0]
        for qubit in qubits:
            self.shared_dict.set_thread_with_id(qubit, t, q)

    def stop_all(self):
        """
        Stops the simulator from running.
        """
        self.shared_dict.send_all_threads(None)
        self.shared_dict.stop_all_threads()
        self.shared_dict.stop_shared_dict()

    def apply_two_qubit_gate(self, gate, q_id1, q_id2):
        self.merge_qubits(q_id1, q_id2)
        q = self.shared_dict.get_queues_for_ids([q_id1])[0]
        q.put([DOUBLE_GATE, gate, q_id1, q_id2])

    def apply_single_gate(self, gate, q_id):
        """
        Applies a single gate to a Qubit.
        """
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([SINGLE_GATE, gate, q_id])

    def give_statevector_for(self, q_id, channel):
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([GIVE_STATEVECTOR, channel])

    def apply_controlled_gate(self, gate, q_id1, q_id2):
        """
        Applies a controlled gate, where the gate is applied to
        q_id1 and controlled by q_id2.

        Args:
            q_id1 (String): Id of the Qubit on which the X gate is applied.
            q_id2 (String): Id of the Qubit which controls the gate.
        """
        self.merge_qubits(q_id1, q_id2)
        q = self.shared_dict.get_queues_for_ids([q_id1])[0]
        q.put([CONTROLLED_GATE, gate, q_id1, q_id2])

    def merge_send(self, q_id, queue, queue2):
        temp_queue = Queue()
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([MERGE_SEND, queue, temp_queue])
        qubits = temp_queue.get()
        # remove all qubits
        for c in qubits:
            self.shared_dict.delete_id_and_check_to_join_thread(c)
        # send the qubits to the main process
        queue2.put(qubits)

    def merge_accept(self, q_id, queue):
        q = self.shared_dict.get_queues_for_ids([q_id])[0]
        q.put([MERGE_ACCEPT, queue])

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
            merge_q = Queue()
            qubits_q = Queue()
            q1.put([MERGE_SEND, merge_q, qubits_q])
            q2.put([MERGE_ACCEPT, merge_q])
            qubits = qubits_q.get()
            self.shared_dict.change_thread_and_queue_of_ids_and_join(
                qubits, q_id2)
