# 空间音频：声像、距离与混音余量

戴耳机转身时声音忽大忽小：声像没有等功率定律，距离衰减与参考距离混用，遮挡不衰减高频，混响区切换突变，多普勒没有钳制，声道布局映射错，距离延迟没补偿，混音没有余量，HRTF 插值跳变，批量混音只提交一半。

## 目录结构

```
README.md
conftest.py
.gitignore
audio/__init__.py
audio/spatial.py
tests/test_spatial.py
```

## 当前状态

`audio/spatial.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_spatial.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. 等功率声像定律
2. 距离衰减按参考距离
3. 遮挡按高频衰减
4. 混响区平滑混合
5. 多普勒速度钳制
6. 声道布局映射
7. 距离延迟补偿
8. 混音总增益留余量
9. HRTF 双耳插值
10. 批量混音统一提交

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `audio/spatial.py`
后 15 条用例应全部通过。
