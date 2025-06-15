import numpy as np

def calculate_mismatch(Ybus, V, theta, P_spec, Q_spec, bus_types):
# 计算 PQ 母线的潮流不平衡量 ΔP 和 ΔQ
    n = len(V)
    P = np.zeros(n)
    Q = np.zeros(n)

    for i in range(n):
        for j in range(n):
            Vi, Vj = V[i], V[j]
            G = np.real(Ybus[i, j])
            B = np.imag(Ybus[i, j])
            theta_ij = theta[i] - theta[j]
            P[i] += Vi * Vj * (G * np.cos(theta_ij) + B * np.sin(theta_ij))
            Q[i] += Vi * Vj * (G * np.sin(theta_ij) - B * np.cos(theta_ij))

    pq_indices = [i for i, t in enumerate(bus_types) if t == "PQ"]
    dP = P_spec[pq_indices] - P[pq_indices]
    dQ = Q_spec[pq_indices] - Q[pq_indices]
    return np.concatenate([dP, dQ])

def build_jacobian(Ybus, V, theta, bus_types):
# 构建雅可比矩阵，仅对 PQ 母线
    n = len(V)
    pq = [i for i, t in enumerate(bus_types) if t == "PQ"]
    npq = len(pq)

    J11 = np.zeros((npq, npq))
    J12 = np.zeros((npq, npq))
    J21 = np.zeros((npq, npq))
    J22 = np.zeros((npq, npq))

    for a in range(npq):
        i = pq[a]
        for b in range(npq):
            j = pq[b]
            Vi, Vj = V[i], V[j]
            G = np.real(Ybus[i, j])
            B = np.imag(Ybus[i, j])
            theta_ij = theta[i] - theta[j]

            if i == j:
                for k in range(n):
                    if k == i: continue
                    Vk = V[k]
                    Gik = np.real(Ybus[i, k])
                    Bik = np.imag(Ybus[i, k])
                    theta_ik = theta[i] - theta[k]
                    J11[a, b] -= Vi * Vk * (Gik * np.sin(theta_ik) - Bik * np.cos(theta_ik))
                    J12[a, b] += Vk * (Gik * np.cos(theta_ik) + Bik * np.sin(theta_ik))
                    J21[a, b] += Vi * Vk * (Gik * np.cos(theta_ik) + Bik * np.sin(theta_ik))
                    J22[a, b] += Vk * (Gik * np.sin(theta_ik) - Bik * np.cos(theta_ik))
                J12[a, b] += 2 * Vi * np.real(Ybus[i, i])
                J22[a, b] -= 2 * Vi * np.imag(Ybus[i, i])
            else:
                J11[a, b] += Vi * Vj * (G * np.sin(theta_ij) - B * np.cos(theta_ij))
                J12[a, b] += Vi * (G * np.cos(theta_ij) + B * np.sin(theta_ij))
                J21[a, b] += Vi * Vj * (G * np.cos(theta_ij) + B * np.sin(theta_ij))
                J22[a, b] += Vi * (G * np.sin(theta_ij) - B * np.cos(theta_ij))

    return np.block([[J11, J12], [J21, J22]])

def solve_powerflow(Ybus, P_spec, Q_spec, V0, theta0, bus_types, tol=1e-6, max_iter=20):
# 使用牛拉法求解潮流方程
    V = V0.copy()
    theta = theta0.copy()
    pq = [i for i, t in enumerate(bus_types) if t == "PQ"]

    for iteration in range(max_iter):
        mismatch = calculate_mismatch(Ybus, V, theta, P_spec, Q_spec, bus_types)
        max_mismatch = np.max(np.abs(mismatch))
        print(f"迭代 {iteration+1} | 最大不平衡量: {max_mismatch:.2e}")

        if max_mismatch < tol:
            print("收敛成功！")
            break

        J = build_jacobian(Ybus, V, theta, bus_types)
        delta = np.linalg.solve(J, mismatch)

        delta_theta = delta[:len(pq)]
        delta_V = delta[len(pq):]

        for k, i in enumerate(pq):
            theta[i] += delta_theta[k]
            V[i] += delta_V[k]
            V[i] = max(V[i], 0.1)  # 防止电压过低

    return V, theta
