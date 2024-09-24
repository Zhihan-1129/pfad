import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import dotenv
import os
from matplotlib.animation import FuncAnimation

# 加载环境变量
dotenv.load_dotenv('F:/SD5913 Creative Programming/Git_Code/pfad/Assignment1_9.25/.env')

# 从环境变量中获取URL
apikey = os.getenv('api_key')
url =  os.getenv('URL')
# 获取空气质量数据
response = requests.get(url)
airdata = json.loads(response.text)
# 提取前20个城市名称和AQI
cities = []
aqis = []
for citydata in airdata['results'][:20]:  # 仅取前20个
    cityname = citydata['location']['name']
    path = citydata['location'].get('path', '')#把城市对应的城市-省份-国家path提取出来
    splitpath = path.split(',')#根据‘，’将path分割成数组
    path = splitpath[2].strip() if len(splitpath) > 2 else ''  # 提取城市所对应的省份名称
    aqi = citydata['aqi']

    citylabel = f"{cityname}, {path}" if path else cityname
    
    cities.append(citylabel)
    aqis.append(int(aqi))  # 将AQI值从字符串转换为整数

# 改颜色
colors = []

# 前15个城市的颜色为渐变的绿色
cmap_green = plt.get_cmap("Greens")
for i in range(15):
    colors.append(cmap_green(i / 15))

# 后5个城市的颜色为橙红色
cmap_orange = plt.get_cmap("Oranges")
for i in range(5):
    colors.append(cmap_orange(0.5 + i / 10))  # 使用中间值加上渐变

# 确保颜色数量与城市数量一致
assert len(colors) == len(cities)

# 改字体
plt.rcParams['font.family'] = 'Calibri'

# 可视化一下
plt.figure(figsize=(12, 8))
bars = plt.barh(cities, aqis, color=colors, edgecolor='#405507')

#改边框颜色
ax = plt.gca()
ax.spines['top'].set_color('#405507')
ax.spines['bottom'].set_color('#405507')
ax.spines['left'].set_color('#405507')
ax.spines['right'].set_color('#405507')

#改边框粗细
ax.spines['top'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)

#改背景颜色
ax.set_facecolor('#f8fff5')

# 给数据加上标签
plt.xlabel('Air Quality Index (The AQI is higher, the worse the air quality is) ', weight='bold', fontsize=16, color='#37570d')
plt.title('Top 20 Cities in China Ranked by AQI ', fontsize=18, weight='bold', color='#37570d')
plt.gca().invert_yaxis()  # 反转Y轴，使AQI从高到低显示

# 给图像加网格线
plt.grid(axis='x', linestyle='--', alpha=0.7)

# 定义刻度和标签
plt.xticks(fontsize=13, color='#37570d')
plt.yticks(fontsize=13, color='#37570d')


# 定义动画函数
def update(frame):
    for i, bar in enumerate(bars):
        bar.set_width(aqis[i] * frame / 20)  # 根据帧数调整柱子宽度

    # 在最后一帧时显示 AQI 值
    if frame == 20:
        for index, value in enumerate(aqis):
            plt.text(value + 0.3, index, str(value), va='center', ha='left', fontsize=13, color='#37570d')

# 创建动画
ani = FuncAnimation(plt.gcf(), update, frames=np.arange(1, 21), interval=100, repeat=False)

# 显示图表
plt.tight_layout()
plt.show()
