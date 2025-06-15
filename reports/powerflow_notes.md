# 潮流计算基础笔记（3节点系统）

## 1. 潮流计算的目标

已知电网结构、负荷、发电，求出每个节点的电压幅值和相角。

## 2. 节点分类

- Slack：电压幅值和相角已知
- PV：有功和电压已知
- PQ：有功和无功已知

## 3. 潮流方程（交流功率）

节点 i 的有功：

$$
P_i = \sum_{j=1}^{n} |V_i||V_j| \left[ G_{ij} \cos(\theta_i - \theta_j) + B_{ij} \sin(\theta_i - \theta_j) \right]
$$

无功：

$$
Q_i = \sum_{j=1}^{n} |V_i||V_j| \left[ G_{ij} \sin(\theta_i - \theta_j) - B_{ij} \cos(\theta_i - \theta_j) \right]
$$

## 4. 3 节点结构简图

[Bus1] --- [Bus2] --- [Bus3]

## 5. 下一步任务

- 手写功率平衡方程（节点2、节点3）
- 写代码验证 Ybus 正确性
- 用牛顿法求解 V2, V3 的电压值