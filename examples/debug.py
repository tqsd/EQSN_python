from eqsn import EQSN
import logging


def main():
    # Activate debugging
    logging.basicConfig(level=logging.DEBUG)
    eqsn = EQSN()

    # create and measure
    id = "Qubit"
    eqsn.new_qubit(id)
    _ = eqsn.measure(id)

    # merge
    id1 = str(1)
    id2 = str(2)
    eqsn.new_qubit(id1)
    eqsn.new_qubit(id2)
    eqsn.merge_qubits(id1, id2)

    eqsn.stop_all()


if __name__ == "__main__":
    main()
