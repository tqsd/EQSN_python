from eqsn import EQSN
import time


def test_get_instance():
    print("test get instance...")
    i1 = EQSN.get_instance()
    i2 = EQSN.get_instance()
    assert i1 == i2
    i1.stop_all()
    print("Test succesfull")


def test_error_at_creating_EQSN_twice():
    error = False
    try:
        _ = EQSN()
        _ = EQSN()
    except:
        error = True
    assert error


if __name__ == "__main__":
    test_get_instance()
    time.sleep(0.1)
    test_error_at_creating_EQSN_twice()
