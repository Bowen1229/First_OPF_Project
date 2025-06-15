# opf_linear_from_json.py
import json
import gurobipy as gp

def load_case_for_opf(filepath):
    """
    从 JSON 文件中加载发电机数据和负荷总需求
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    generators = data["generators"]
    n_gen = len(generators)
    pmin = [gen["pmin"] for gen in generators]
    pmax = [gen["pmax"] for gen in generators]
    cost = [gen["cost"] for gen in generators]

    # 假设每个母线有 Pd 表示有功负荷需求
    load = sum(bus.get("Pd", 0) for bus in data["buses"])

    return n_gen, pmin, pmax, cost, load


def solve_linear_opf(n_gen, pmin, pmax, cost, load):
    """
    构建并求解线性最优潮流问题
    """
    model = gp.Model("opf_linear")
    Pg = model.addVars(n_gen, lb=pmin, ub=pmax, name="Pg")

    model.setObjective(
        gp.quicksum(cost[i] * Pg[i] for i in range(n_gen)),
        gp.GRB.MINIMIZE
    )

    model.addConstr(
        gp.quicksum(Pg[i] for i in range(n_gen)) == load,
        name="PowerBalance"
    )

    model.optimize()

    result = {}
    for i in range(n_gen):
        result[f"Pg[{i}]"] = Pg[i].X
    result["OptimalCost"] = model.ObjVal
    return result


# 主程序入口
if __name__ == "__main__":
    # 自动从 JSON 文件读取模型参数
    filepath = "../data/3bus_with_gen.json"
    n_gen, pmin, pmax, cost, load = load_case_for_opf(filepath)

    # 求解 OPF
    result = solve_linear_opf(n_gen, pmin, pmax, cost, load)

    # 打印结果
    print("\n最优发电计划：")
    for k, v in result.items():
        if "Pg" in k:
            print(f"{k} = {v:.2f} MW")
    print(f"\n最小总发电成本：{result['OptimalCost']:.4f} $/h")
