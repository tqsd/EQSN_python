import numpy as np
import logging
from copy import deepcopy as dp
import random
import sys

NONE = 0
SINGLE_GATE = 1
CONTROLLED_GATE = 2
MEASURE = 3
MERGE_ACCEPT = 4
MERGE_SEND = 5
MEASURE_NON_DESTRUCTIVE = 7
NEW_QUBIT = 8
ADD_MERGED_QUBITS_TO_DICT = 9
GIVE_STATEVECTOR = 10
DOUBLE_GATE = 11


class QubitThread(object):

    def __init__(self, q_id, queue):
        """
        Args:
            q_id (String): Name of the qubit
            queue (Queue): Queue for receiving commands from main thread.
        """
        # set new seed for random number generator
        local_random = random.Random()
        new_seed = local_random.randrange(1, 100000)
        np.random.seed(new_seed)

        # List of qubits in this thread
        self.qubits = [q_id]

        # receive queue for operations to perform
        self.queue = queue

        # init qubit in state |0>
        self.qubit = np.zeros(2, dtype=np.csingle)
        self.qubit[0] = 1

        logging.debug("Qubit thread with qubit %s has been created.", q_id)

    def apply_single_gate(self, mat, q_id):
        """
        Applys a single gate to a qubit.

        Args:
            mat (np.array): 2x2 unitary array.
            id (String): Qubit on which the gate should be applied to.
        """
        apply_mat = mat
        nr = self.qubits.index(q_id)
        total_amount = len(self.qubits)
        before = nr
        after = total_amount - nr - 1
        if before > 0:
            apply_mat = np.kron(np.eye(2 ** before), apply_mat)
        if after > 0:
            apply_mat = np.kron(apply_mat, np.eye(2 ** after))
        self.qubit = np.dot(apply_mat, self.qubit)

    def give_statevector(self, channel):
        channel.put((dp(self.qubits), dp(self.qubit)))

    def apply_controlled_gate(self, mat, q_id1, q_id2):
        """
        Apply a controlled gate to
        """
        first_mat = 1
        second_mat = 1
        nr1 = self.qubits.index(q_id1)
        nr2 = self.qubits.index(q_id2)
        min_nr = min(nr1, nr2)
        max_nr = max(nr1, nr2)
        if min_nr == nr1:
            # first_mat = mat
            pass
        total_amount = len(self.qubits)
        before = min_nr
        after = total_amount - max_nr - 1
        mid = total_amount - before - after - 2
        if before > 0:
            first_mat = np.eye(2 ** before)
            second_mat = np.eye(2 ** before)
        # Apply first part of Matrix
        if min_nr == nr1:
            first_mat = np.kron(first_mat, np.eye(2))
            second_mat = np.kron(second_mat, mat)
        else:
            first_mat = np.kron(first_mat, np.array([[1, 0], [0, 0]]))
            second_mat = np.kron(second_mat, np.array([[0, 0], [0, 1]]))

        if mid > 0:
            first_mat = np.kron(first_mat, np.eye(2 ** mid))
            second_mat = np.kron(second_mat, np.eye(2 ** mid))
        # Apply second part of Matrix
        if min_nr == nr1:
            first_mat = np.kron(first_mat, np.array([[1, 0], [0, 0]]))
            second_mat = np.kron(second_mat, np.array([[0, 0], [0, 1]]))
        else:
            first_mat = np.kron(first_mat, np.eye(2))
            second_mat = np.kron(second_mat, mat)

        if after > 0:
            first_mat = np.kron(first_mat, np.eye(2 ** after))
            second_mat = np.kron(second_mat, np.eye(2 ** after))
        apply_mat = first_mat + second_mat
        self.qubit = np.dot(apply_mat, self.qubit)

    def merge_accept(self, channel):
        """
        Receive another process to merge it with this one.
        """
        ids = channel.get()
        vector = channel.get()
        self.qubits = self.qubits + ids
        self.qubit = np.kron(self.qubit, vector)
        logging.debug("Qubit Thread merged, new qubits are %r", self.qubits)

    def merge_send(self, channel, chanel2):
        """
        Send own process data to another process and suicide.
        """
        channel.put(dp(self.qubits))
        channel.put(dp(self.qubit))
        chanel2.put(dp(self.qubits))
        return

    def swap_qubits(self, q_id1, q_id2):
        """
        Swaps the position of qubit q_id1 with q_id2
        in the statevector.
        """
        def cnot(q_id1, q_id2):
            mat = np.asarray([[0, 1], [1, 0]])
            self.apply_controlled_gate(mat, q_id1, q_id2)

        # Check if they are the same ids
        if q_id1 == q_id2:
            return

        # Perform swap
        cnot(q_id1, q_id2)
        cnot(q_id2, q_id1)
        cnot(q_id1, q_id2)
        # Change ordering in the list
        i1 = self.qubits.index(q_id1)
        i2 = self.qubits.index(q_id2)
        self.qubits[i1], self.qubits[i2] = self.qubits[i2], self.qubits[i1]

    def apply_two_qubit_gate(self, mat, q_id1, q_id2):
        # Bring the qubits in the right order
        i2 = self.qubits.index(q_id2)
        if i2 > 0:
            new_i1 = i2-1
            self.swap_qubits(q_id1, self.qubits[new_i1])
        else:
            self.swap_qubits(q_id1, self.qubits[0])
            self.swap_qubits(q_id2, self.qubits[1])
        apply_mat = mat
        nr1 = self.qubits.index(q_id1)
        total_amount = len(self.qubits)
        before = nr1
        after = total_amount - nr1 - 2
        if before > 0:
            apply_mat = np.kron(np.eye(2 ** before), apply_mat)
        if after > 0:
            apply_mat = np.kron(apply_mat, np.eye(2 ** after))
        self.qubit = np.dot(apply_mat, self.qubit)

    def measure_non_destructive(self, q_id, ret_channel):
        """
        Perform a non destructive measurement on qubit with the id.
        """
        # determine probability for |1>
        measure_vec = np.array([1, 0], dtype=np.csingle)
        nr = self.qubits.index(q_id)
        total_amount = len(self.qubits)
        before = nr
        after = total_amount - nr - 1
        if before > 0:
            measure_vec = np.kron(np.ones(2 ** before), measure_vec)
        if after > 0:
            measure_vec = np.kron(measure_vec, np.ones(2 ** after))
        pr_0 = np.multiply(measure_vec, self.qubit)
        pr_0 = abs(np.dot(pr_0, pr_0))
        if pr_0 > 1.0:
            pr_0 = 1.0
        elif pr_0 < 0.0:
            pr_0 = 0.0
        meas_res = np.random.binomial(1, 1.0 - pr_0)
        reduction_mat = None
        if meas_res == 0:
            # |0> has been measured
            ret_channel.put(0)
            reduction_mat = np.array([[1, 0], [0, 0]], dtype=np.csingle)
        else:
            # |1> has been measured
            ret_channel.put(1)
            reduction_mat = np.array([[0, 0], [0, 1]], dtype=np.csingle)
        if before > 0:
            reduction_mat = np.kron(
                np.eye(2 ** before, dtype=np.csingle), reduction_mat)
        if after > 0:
            reduction_mat = np.kron(
                reduction_mat, np.eye(2 ** after, dtype=np.csingle))
        # apply measurement result to state vector
        self.qubit = np.dot(reduction_mat, self.qubit)
        # renormalize the qubit vector
        norm = np.linalg.norm(self.qubit)
        self.qubit = self.qubit / norm

    def measure(self, q_id, ret_channel):
        """
        Perform a destructive measurement on qubit with the id.
        """
        # determine probability for |1>
        measure_vec = np.array([1, 0], dtype=np.csingle)
        nr = self.qubits.index(q_id)
        total_amount = len(self.qubits)
        before = nr
        after = total_amount - nr - 1
        if before > 0:
            measure_vec = np.kron(np.ones(2 ** before), measure_vec)
        if after > 0:
            measure_vec = np.kron(measure_vec, np.ones(2 ** after))
        pr_0 = np.multiply(measure_vec, self.qubit)
        pr_0 = abs(np.dot(pr_0, pr_0))
        if pr_0 > 1.0:
            pr_0 = 1.0
        elif pr_0 < 0.0:
            pr_0 = 0.0
        meas_res = np.random.binomial(1, 1.0 - pr_0)
        reduction_mat = None
        if meas_res == 0:
            # |0> has been measured
            ret_channel.put(0)
            reduction_mat = np.array([1, 0], dtype=np.csingle)
        else:
            # |1> has been measured
            ret_channel.put(1)
            reduction_mat = np.array([0, 1], dtype=np.csingle)
        if before > 0:
            reduction_mat = np.kron(
                np.eye(2 ** before, dtype=np.csingle), reduction_mat)
        if after > 0:
            reduction_mat = np.kron(
                reduction_mat, np.eye(2 ** after, dtype=np.csingle))
        self.qubits.remove(q_id)
        if total_amount == 1:
            # it was the last qubit, just terminate this process
            return
        # remove measured qubit from qubit state vector
        self.qubit = np.dot(reduction_mat, self.qubit)
        # renormalize the qubit vector
        norm = np.linalg.norm(self.qubit)
        self.qubit = self.qubit / norm

    def run(self):
        """
        Run in loop and wait to receive tasks to perform.
        """
        while True:
            item = self.queue.get()
            if item is None:
                return
            elif item[0] == SINGLE_GATE:
                self.apply_single_gate(item[1], item[2])
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
                self.merge_send(item[1], item[2])
                return
            elif item[0] == MEASURE_NON_DESTRUCTIVE:
                self.measure_non_destructive(item[1], item[2])
            elif item[0] == GIVE_STATEVECTOR:
                self.give_statevector(item[1])
            elif item[0] == DOUBLE_GATE:
                self.apply_two_qubit_gate(item[1], item[2], item[3])
            else:
                raise ValueError("Command does not exist!")
