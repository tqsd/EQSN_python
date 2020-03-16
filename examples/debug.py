from eqsn import EQSN
import logging


def main():
    # Activate debugging
    logging.basicConfig(level=logging.DEBUG)
    eqsn = EQSN()
    id = "Qubit"
    eqsn.new_qubit(id)
    _ = eqsn.measure(id)


if __name__ == "__main__":
    main()
