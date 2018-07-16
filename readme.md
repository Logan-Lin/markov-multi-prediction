# 多候选马尔可夫轨迹预测

## 功能

- 导入csv数据并计算马尔可夫矩阵
- 根据给定历史序列给出预测
- 每个点的预测都能给出多个候选值
- 历史轨迹长度、预测轨迹长度和候选值数量均可调整

## 使用

### 初始化

```
    markov = Markov(his_count=1, pre_count=3, test_count=3, tol=3)
```python

- `his_count`为历史轨迹长度
- `pre_count`为预测轨迹长度
- `test_count`为csv文件中每一行数据需要留作测试集的长度（取最后`test_count`数量的点作测试集）
- `tol`为候选值数量

### 读入csv文件

    markov.read_csv('trajectory100000.csv')

### 使用csv文件数据进行测试

    acc = markov.test_csv('trajectory100000.csv')

### 导出预测序列

    markov.write_pre('trajectory100000.csv', 'result.csv')
