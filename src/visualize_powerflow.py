# visualize_powerflow.py

import json
import matplotlib.pyplot as plt

def plot_voltage_magnitude(V, bus_ids=None):
# 绘制节点电压幅值柱状图
# V: 电压幅值列表（如 [1.0, 0.98, 1.01]）
# bus_ids: 可选，节点编号列表（如 ['Bus 1', 'Bus 2', ...]）
    if bus_ids is None:
        bus_ids = [f"Bus {i+1}" for i in range(len(V))]

    plt.figure(figsize=(8, 5))
    plt.bar(bus_ids, V)
    plt.ylabel("Voltage Magnitude (p.u.)")
    plt.title("Bus Voltage Profile")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def add_generators_to_case(input_file, output_file, generators,loads):

# 向已有的电网数据中添加发电机信息，并保存为新的 JSON 文件
# input_file: 原始 JSON 文件路径
# output_file: 修改后输出文件路径
# generators: 发电机信息列表，如：[{"bus": 1, "pmin": 0, "pmax": 6, "cost": 10}]
    with open(input_file, 'r') as f:
        case = json.load(f)

    case["generators"] = generators

    # 输入每个 bus 的 Pd（负荷）
    for bus in case["buses"]:
        bus_id = bus["id"]
        if str(bus_id) in loads:
            bus["Pd"] = loads[str(bus_id)]
        else:
            bus["Pd"] = 0  # 没指定的就设为 0

    with open(output_file, 'w') as f:
        json.dump(case, f, indent=2)

    print(f"已生成带发电机的数据文件：{output_file}")

# 使用例
if __name__ == "__main__":
    # 1. 绘图：潮流计算后的节点电压（数据为自定的）
    voltage_magnitudes = [1.00, 1.00, 1.00]
    plot_voltage_magnitude(voltage_magnitudes)

    # 2. 添加发电机信息到数据文件中
    input_path = "../data/3bus.json" 
    output_path = "../data/3bus_with_gen.json"
    generators = [
    {"bus": 1, "pmin": 0, "pmax": 6, "cost": 0.015},
    {"bus": 3, "pmin": 0, "pmax": 4, "cost": 0.03}
    ]

    loads = {
        "2": 5,
        "3": 3
    }

    add_generators_to_case(input_path, output_path, generators, loads)
