============
Introduction
============

EQSN is a quantum simulator for networks. It is developed as a backend for
QuNetSim, but can also be used as a standalone library.

At the moment, EQSN is still under development and might be buggy. If you
find any bugs, please open a issue on the github page.

The EQSN API is intended to be threadsafe. A new Qubit is created in its own
process. As soon as a two qubit gate is applied, the qubits are merged into one
process and their starevector is merges, using the kronecker product.

Gates and other commands are send over process channels to the qubits.
