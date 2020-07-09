from eqsn import EQSN
import time


def test_x_gate():
    q_sim = EQSN.get_instance()
    _id = str(10)
    q_sim.new_qubit(_id)
    q_sim.X_gate(_id)
    res = q_sim.measure(_id)
    assert res == 1
    q_sim.stop_all()


def test_y_gate():
    q_sim = EQSN.get_instance()
    _id = str(11)
    q_sim.new_qubit(_id)
    q_sim.Y_gate(_id)
    q_sim.Y_gate(_id)
    res = q_sim.measure(_id)
    assert res == 0
    q_sim.stop_all()


def test_z_gate():
    q_sim = EQSN.get_instance()
    _id = str(10)
    q_sim.new_qubit(_id)
    q_sim.Z_gate(_id)
    q_sim.Z_gate(_id)
    res = q_sim.measure(_id)
    assert res == 0
    q_sim.stop_all()


def test_H_gate():
    q_sim = EQSN.get_instance()
    _id = str(10)
    q_sim.new_qubit(_id)
    q_sim.H_gate(_id)
    q_sim.H_gate(_id)
    res = q_sim.measure(_id)
    assert res == 0
    q_sim.stop_all()


def test_T_gate():
    q_sim = EQSN.get_instance()
    _id = str(10)
    q_sim.new_qubit(_id)
    q_sim.T_gate(_id)
    res = q_sim.measure(_id)
    assert res == 0
    _id = str(11)
    q_sim.new_qubit(_id)
    q_sim.H_gate(_id)
    q_sim.T_gate(_id)
    q_sim.T_gate(_id)
    q_sim.T_gate(_id)
    q_sim.T_gate(_id)
    q_sim.H_gate(_id)
    res = q_sim.measure(_id)
    assert res == 1
    q_sim.stop_all()


def test_S_gate():
    q_sim = EQSN.get_instance()
    _id = str(11)
    q_sim.new_qubit(_id)
    q_sim.H_gate(_id)
    q_sim.S_gate(_id)
    q_sim.S_gate(_id)
    q_sim.H_gate(_id)
    res = q_sim.measure(_id)
    assert res == 1
    q_sim.stop_all()


def test_K_gate():
    q_sim = EQSN.get_instance()
    _id = str(11)
    q_sim.new_qubit(_id)
    q_sim.H_gate(_id)
    q_sim.K_gate(_id)
    q_sim.K_gate(_id)
    q_sim.H_gate(_id)
    res = q_sim.measure(_id)
    assert res == 0
    q_sim.stop_all()


def test_measure():
    q_sim = EQSN.get_instance()
    _id = str(10)
    q_sim.new_qubit(_id)
    res = q_sim.measure(_id)
    assert res == 0
    q_sim.stop_all()


if __name__ == "__main__":
    test_list = [test_x_gate,
                 test_y_gate,
                 test_z_gate,
                 test_H_gate,
                 test_T_gate,
                 test_S_gate,
                 test_K_gate,
                 test_measure]
    for func in test_list:
        func()
        time.sleep(0.1)
