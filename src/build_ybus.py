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

def print_Ybus(Y):
    print("Ybus 导纳矩阵:")
    for row in Y:
        print(["{:.2f}".format(val) for val in row])

if __name__ == "__main__":
    case = load_case("../data/3bus.json")
    Ybus = build_Ybus(case)
    print_Ybus(Ybus)
