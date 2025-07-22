import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# A4尺寸（单位：pt）
A4_WIDTH = 595
A4_HEIGHT = 842

# 多个框坐标
bboxes = [
    [36, 158, 523, 234],
    [36, 159, 522, 172],
    [36, 159, 522, 172],
    [35, 174, 522, 189],
    [35, 174, 465, 189],
    [465, 174, 485, 187], # 百分号
    [485, 174, 522, 189],
    [35, 190, 522, 205],
    [35, 190, 522, 205],
    [36, 206, 522, 219],
    [36, 206, 522, 219],
    [36, 222, 427, 235],
    [36, 222, 427, 235],

    [83, 459, 279, 490],
    [83, 459, 279, 490],
    [83, 459, 279, 490],
    [83, 459, 279, 490],
    [104, 432, 260, 451],
    [104, 432, 260, 451],
    [104, 432, 260, 451]
]

fig, ax = plt.subplots(figsize=(A4_WIDTH/100, A4_HEIGHT/100), dpi=100)
ax.set_xlim(0, A4_WIDTH)
ax.set_ylim(A4_HEIGHT, 0)  # y轴反向，符合PDF坐标习惯

# 绘制所有矩形框
for bbox in bboxes:
    rect = Rectangle((bbox[0], bbox[1]), bbox[2]-bbox[0], bbox[3]-bbox[1],
                    linewidth=2, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

# 去掉坐标轴
ax.axis('off')

plt.show()