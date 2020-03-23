class ProcessPicker(object):
    """
    Decides which process allocates new Qubits.
    """

    @staticmethod
    def get_instance():
        if ProcessPicker.__instance is None:
            return ProcessPicker()
        return ProcessPicker.__instance

    def __init__(self, cpu_count, process_queue_list):
        if ProcessPicker.__instance is not None:
            raise ValueError(
                "Use get instance to get the Process picker class.")
        self.amount_processes = cpu_count
        self.pointer = 0
        self.process_queue_list = process_queue_list

    def get_next_process_queue(self):
        """
        Called in threads may override pointer, but we do not care, since
        the pointer value is not essential.
        """
        res_q = self.process_queue_list[self.pointer % self.amount_processes]
        self.pointer += 1
        return res_q
