# 3节点系统

## 节点分类

- Slack：电压幅值和相角已知
- PV：有功和电压已知
- PQ：有功和无功已知

## 潮流方程（交流功率）

节点 i 的有功：

$$
P_i = \sum_{j=1}^{n} |V_i||V_j| \left[ G_{ij} \cos(\theta_i - \theta_j) + B_{ij} \sin(\theta_i - \theta_j) \right]
$$

无功：

$$
Q_i = \sum_{j=1}^{n} |V_i||V_j| \left[ G_{ij} \sin(\theta_i - \theta_j) - B_{ij} \cos(\theta_i - \theta_j) \right]
$$

## 节点结构简图

[Bus1] --- [Bus2] --- [Bus3]
