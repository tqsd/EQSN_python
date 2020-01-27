import numpy as np
from copy import deepcopy as dp

NONE = 0
SINGLE_GATE = 1
CONTROLLED_GATE = 2
MEASURE = 3
MERGE_ACCEPT = 4
MERGE_SEND = 5
GIVE_QUBITS_AND_TERMINATE = 6

class QubitThread(object):


    def __init__(self, q_id, queue):

        # List of qubits in this thread
        self.qubits = [q_id]

        # receive queue for operations to perform
        self.queue = queue

        # init qubit in state |0>
        self.qubit = np.zeros(2, dtype=np.csingle)
        self.qubit[0] = 1

    def apply_single_gate(self, mat, id):
        apply_mat = mat
        nr = self.qubits.index(id)
        total_amount = len(self.qubits)
        before = nr
        after = total_amount - nr -1
        if before > 0:
            apply_mat = np.kron(np.eye(2**before), apply_mat)
        if after > 0:
            apply_mat = np.kron(apply_mat, np.eye(2**after))
        self.qubit = np.dot(apply_mat, self.qubit)

    def apply_controlled_gate(self, mat, id1, id2):
        first_mat = 1
        second_mat = 1
        nr1 = self.qubits.index(id1)
        nr2 = self.qubits.index(id2)
        min_nr = min(nr1, nr2)
        max_nr = max(nr1, nr2)
        if min_nr == nr1:
            # first_mat = mat
            pass
        total_amount = len(self.qubits)
        before = min_nr
        after = total_amount - max_nr -1
        mid = total_amount - before - after - 2
        if before > 0:
            first_mat = np.eye(2**before)
            second_mat = np.eye(2**before)
        # Apply first part of Matrix
        if min_nr == nr1:
            first_mat = np.kron(firt_mat, np.eye(2))
            second_mat = np.kron(second_mat, mat)
        else:
            first_mat = np.kron(first_mat, np.array([[1,0],[0,0]]))
            second_mat = np.kron(second_mat, np.array([[0,0],[0,1]]))

        if mid > 0:
            first_mat = np.kron(first_mat, np.eye(2**mid))
            second_mat = np.kron(second_mat, np.eye(2**mid))
        # Apply second part of Matrix
        if min_nr == nr1:
            first_mat = np.kron(first_mat, np.array([[1,0],[0,0]]))
            second_mat = np.kron(second_mat, np.array([[0,0],[0,1]]))
        else:
            first_mat = np.kron(first_mat, np.eye(2))
            second_mat = np.kron(second_mat, mat)

        if after > 0:
            first_mat = np.kron(first_mat, np.eye(2**after))
            second_mat = np.kron(second_mat, np.eye(2**after))
        apply_mat = first_mat + second_mat
        self.qubit = np.dot(apply_mat, self.qubit)

    def merge_accept(self, channel):
        ids = channel.get()
        vector = channel.get()
        self.qubits = self.qubits + ids
        self.qubit = np.kron(self.qubit, vector)

    def merge_send(self, channel):
        channel.put(dp(self.qubits))
        channel.put(dp(self.qubit))
        return

    def send_qubits(self, channel):
        channel.put(dp(self.qubits))
        return

    def measure(self, id, ret_channel):
        # determine probability for |1>
        measure_vec = np.array([1,0], dtype=np.csingle)
        nr = self.qubits.index(id)
        total_amount = len(self.qubits)
        before = nr
        after = total_amount - nr -1
        if before > 0:
            measure_vec = np.kron(np.ones(2**before), measure_vec)
        if after > 0:
            measure_vec = np.kron(measure_vec, np.ones(2**after))
        pr_0 = np.multiply(measure_vec, self.qubit)
        pr_0 = np.dot(pr_0, pr_0)
        meas_res = np.random.binomial(1, 1.0 - pr_0.real)
        reduction_mat = None
        if meas_res == 0:
            # |0> has been measured
            ret_channel.put(0)
            reduction_mat = np.array([1,0], dtype=np.csingle)
        else:
            # |1> has been measured
            ret_channel.put(1)
            reduction_mat = np.array([0,1], dtype=np.csingle)
        if before > 0:
            reduction_mat = np.kron(np.eye(2**before, dtype=np.csingle), reduction_mat)
        if after > 0:
            reduction_mat = np.kron(reduction_mat, np.eye(2**after, dtype=np.csingle))
        self.qubits.remove(id)
        if total_amount == 1:
            # it was the last qubit, just terminate this process
            return
        # remove measured qubit from qubit state vector
        self.qubit = np.dot(reduction_mat, self.qubit)
        # renormalize the qubit vector
        norm = np.linalg.norm(self.qubit)
        self.qubit = self.qubit/norm


    def run(self):
        amount_single_gate = 0
        while True:
            item = self.queue.get()
            if item is None:
                return
            elif item[0] == SINGLE_GATE:
                self.apply_single_gate(item[1], item[2])
                amount_single_gate += 1
            elif item[0] == CONTROLLED_GATE:
                self.apply_controlled_gate(item[1], item[2], item[3])
            elif item[0] == MEASURE:
                self.measure(item[1], item[2])
                # no qubit left, terminate
                if len(self.qubits) == 0:
                    return
            elif item[0] == MERGE_ACCEPT:
                self.merge_accept(item[1])
            elif item[0] == MERGE_SEND:
                self.merge_send(item[1])
            elif item[0] == GIVE_QUBITS_AND_TERMINATE:
                self.send_qubits(item[1])
                return
            else:
                raise ValueError("Command does not exist!")
