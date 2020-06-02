###############
Worker Process
###############

The worker process is a parent of a set of qubit threads. It is responsible to
increase the concurrency of the EQSN package. Using a dictionary, it keeps track
of all qubits within its thread and provides an interface for the gates class.


.. automodule:: eqsn.worker_process
   :members:
