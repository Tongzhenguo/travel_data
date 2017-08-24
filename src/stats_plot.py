import pandas as pd
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

d = pd.read_csv('../data/stats.csv')
d.index = d['﻿name']
plt = d[['score']].plot(kind='barh').get_figure()
plt.savefig('p1.png')


# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.show()

plt = d[['comments']].plot(kind='barh').get_figure()
plt.savefig('p2.png')