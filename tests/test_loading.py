import sys
import os
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loading import get_agents


def test_get_agents1():
    agent_classes = get_agents(os.path.join('tests', 'input', 'agents1.csv'))
    expected = {
        'vehicle': 'vehicle.tesla.model3',
        'agent_type': 'traffic_manager',
        'number': 1,
        'hvac': 0.0,
        'ev_params': {
            'capacity': 50.0,
            'A_f': 2.3316,
            'gravity': 9.8066,
            'C_r': 1.75,
            'c_1': 0.0328,
            'c_2': 4.575,
            'rho_Air': 1.2256,
            'C_D': 0.28,
            'motor_efficiency': 0.91,
            'driveline_efficiency': 0.92,
            'braking_alpha': 0.0411,
        }
    }
    try:
        assert len(agent_classes) == 1
        assert agent_classes[0]['vehicle'] == expected['vehicle']
        assert agent_classes[0]['agent_type'] == expected['agent_type']
        assert agent_classes[0]['number'] == expected['number']
        assert agent_classes[0]['hvac'] == expected['hvac']
        assert agent_classes[0]['ev_params'] == expected['ev_params']
        assert agent_classes[0] == expected
    except AssertionError:
        traceback.print_exc()
        print(f"{agent_classes=}")
        print()
        return False
    return True


def test_get_agents2():
    agent_classes = get_agents(os.path.join('tests', 'input', 'agents2.csv'))
    try:
        assert len(agent_classes) == 2
        assert agent_classes[0]['vehicle'] == 'vehicle.tesla.model3'
        assert agent_classes[1]['agent_type'] == 'cautious_behavior'
    except AssertionError:
        traceback.print_exc()
        print(f"{agent_classes=}")
        print()
        return False
    return True


if __name__ == "__main__":
    tests = (
        test_get_agents1, 
        test_get_agents2, 
    )
    success = 0
    total = 0
    for test in tests:
        if test():
            success += 1
        total += 1
    print(f"Passed {success} out of {total} tests.")
