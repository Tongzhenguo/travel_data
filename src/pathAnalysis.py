# coding=utf-8
import pandas as pd
'''
    旅游路线分析,调用networkx包进行关联展示
'''

data= pd.read_csv('../data/out.csv')
pairs = []
for path in data['pois'].values:
    nodes = path.split('/')
    for i in range( len(nodes)-1 ):
        if nodes[i]=='上海' or nodes[i+1]=='上海':continue
        if nodes[i]==nodes[i+1]:continue
        pairs.append( nodes[i]+'_'+nodes[i+1] )
df = pd.value_counts( pairs ).to_frame()
df = df.reset_index()
df.columns = ['pair','freq']
# df['pair'] = df['pair'].astype(str)
a = df[df['pair'].str.startswith('外滩')].head(20)


import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# colors = ['red', 'yellow', 'yellow', 'yellow']
#有向图
DG = nx.DiGraph()
#添加边，数据格式为列表
for t2 in a.values:
    nodes = t2[0].split('_')
    DG.add_edge( nodes[0],nodes[1],weight=float(t2[1]) )
    # DG.add_weighted_edges_from([('田子坊', '迪士尼',5), ('田子坊', '城隍庙',4.5), ('田子坊', '外滩',3)])
# DG.add_edges_from()
#作图，设置节点名显示,节点大小，节点颜色
'''
pos（布局）参数，
circular_layout：节点在一个圆环上均匀分布
random_layout：节点随机分布
shell_layout：节点在同心圆上分布
spring_layout： 用Fruchterman-Reingold算法排列节点（这个算法我不了解，样子类似多中心放射状）
spectral_layout：根据图的拉普拉斯特征向量排列节点？我也不是太明白
'''
nx.draw(DG,pos=nx.circular_layout(DG),with_labels=True, node_size=900)#, node_color = colors
plt.show()


df.to_csv('../data/pair_freq.csv')