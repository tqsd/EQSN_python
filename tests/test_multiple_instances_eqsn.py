from eqsn import EQSN
import time


def test_get_instance():
    i1 = EQSN.get_instance()
    i2 = EQSN.get_instance()
    assert i1 == i2
    i1.stop_all()
    i2.stop_all()


def test_error_at_creating_EQSN_twice():
    error = False
    i1 = None
    try:
        i1 = EQSN()
        _ = EQSN()
    except:
        error = True
    assert error
    i1.stop_all()


if __name__ == "__main__":
    test_get_instance()
    time.sleep(0.1)
    test_error_at_creating_EQSN_twice()
    exit(0)
