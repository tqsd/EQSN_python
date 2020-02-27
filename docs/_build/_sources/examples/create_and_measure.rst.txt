Create Qubit and Measure
-------------------------

..  code-block:: python
    :linenos:

    import eqsn

    # Create a Qubit with id A
    eqsn.new_qubit('A')

    # Measure the Qubit with id A
    m = eqsn.measure('A')
    
    print("Measured Qubit with id 'A' with result %d." % m)
