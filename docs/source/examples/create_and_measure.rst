Create Qubit and Measure
-------------------------

..  code-block:: python
    :linenos:

    from eqsn import EQSN

    # create the EQSN control object
    eqsn = EQSN()

    # Create a Qubit with id A
    eqsn.new_qubit('A')

    # Measure the Qubit with id A
    m = eqsn.measure('A')

    print("Measured Qubit with id 'A' with result %d." % m)
