EPR State Creation
-------------------

Below, an example is shown, how an EPR state can be created.

..  code-block:: python
    :linenos:

    from eqsn import EQSN

    # create EQSN control object
    eqsn = EQSN()

    # Create two Qubits, with ids A and B
    eqsn.new_qubit('A')
    eqsn.new_qubit('B')

    # Apply a Hadamard gate to qubit B
    eqsn.H_gate('B')

    # Apply a cnot gate, applied to A, controlled by B
    eqsn.cnot_gate('A', 'B')

    # Measure both Qubits
    m1 = eqsn.measure('A')
    m2 = eqsn.measure('B')

    print("measured %d and %d." % (m1, m2))
