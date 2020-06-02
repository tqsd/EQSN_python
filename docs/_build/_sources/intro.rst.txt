============
Introduction
============

EQSN is a quantum simulator for networks. It is developed as a backend for
QuNetSim, but can also be used as a standalone library.

At the moment, EQSN is still under development and might be buggy. If you
find any bugs, please open a issue on the github page.

The EQSN API is intended to be threadsafe. A new qubit is created in a thread,
parented by a parent process. As soon as a two qubit gate is applied, the
qubits are merged into one
thread and their statevector is merged.

Gates and other commands are send over process channels to the qubits.
