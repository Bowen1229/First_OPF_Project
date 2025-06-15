import numpy as np
from build_ybus import build_Ybus, load_case
from newton_solver import solve_powerflow

# 1.加载网络数据并确保 Slack 节点排在第一位
case = load_case("../data/3bus.json")
case["buses"].sort(key=lambda x: 0 if x["type"] == "Slack" else 1)  # 强制排在第一个
Ybus = build_Ybus(case)

# 2.第二步：设定初始条件 
n_bus = len(case["buses"])
V0 = np.array([1.0, 0.95, 0.95])        # 初始电压幅值
theta0 = np.zeros(n_bus)               # 初始电压相角

# 节点类型、负荷 
bus_types = [bus["type"] for bus in case["buses"]]
P_spec = np.array([0.0, -0.3, -0.3])
Q_spec = np.array([0.0, -0.1, -0.1])

# 3.执行牛顿潮流迭代 
V, theta = solve_powerflow(Ybus, P_spec, Q_spec, V0, theta0, bus_types)

# 4.输出结果 
print("\n最终每个母线电压与相角：")
for i in range(n_bus):
    print(f"Bus {i+1}: |V| = {V[i]:.4f} p.u., θ = {np.degrees(theta[i]):.2f}°")
