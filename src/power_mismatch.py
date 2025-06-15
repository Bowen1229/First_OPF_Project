import json
import numpy as np

def load_case(filepath):
    with open(filepath, 'r') as f:
        case = json.load(f)
    return case

def build_Ybus(case):
    n = len(case["buses"])
    Y = np.zeros((n, n), dtype=complex)
    for br in case["branches"]:
        i = br["from"] - 1
        j = br["to"] - 1
        z = complex(br["r"], br["x"])
        y = 1 / z
        Y[i, i] += y
        Y[j, j] += y
        Y[i, j] -= y
        Y[j, i] -= y
    return Y

def calculate_power_injection(Ybus, V, theta, i):
    Pi = 0
    Qi = 0
    n = len(V)

    for j in range(n):
        G = Ybus[i, j].real
        B = Ybus[i, j].imag
        angle = theta[i] - theta[j]

        Pi += V[i] * V[j] * (G * np.cos(angle) + B * np.sin(angle))
        Qi += V[i] * V[j] * (G * np.sin(angle) - B * np.cos(angle))

    return Pi, Qi

def calculate_power_mismatch(Ybus, V, theta, P_spec, Q_spec, pq_buses):
    mismatches = []

    for i in pq_buses:
        Pi, Qi = calculate_power_injection(Ybus, V, theta, i)
        dP = P_spec[i] - Pi
        dQ = Q_spec[i] - Qi
        mismatches.extend([dP, dQ])

    return np.array(mismatches)

if __name__ == "__main__":
    # 载入网络数据
    case = load_case("../data/3bus.json")
    Ybus = build_Ybus(case)

    # 初始猜测：电压为1.0，角度为0
    V = np.array([1.0, 1.0, 1.0])
    theta = np.array([0.0, 0.0, 0.0])

    # 指定功率需求（负载），索引0是Slack，不处理
    P_spec = np.array([0.0, -1.0, -1.0])
    Q_spec = np.array([0.0, -0.5, -0.5])
    pq_buses = [1, 2]  # Bus 2 和 Bus 3

    # 计算不平衡量
    mismatch = calculate_power_mismatch(Ybus, V, theta, P_spec, Q_spec, pq_buses)
    print("潮流功率不平衡量 ΔP 和 ΔQ:")
    print(mismatch)
