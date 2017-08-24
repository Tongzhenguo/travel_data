# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

colors = ['red', 'yellow', 'yellow', 'yellow']
#有向图
DG = nx.DiGraph()
#一次性添加多节点，输入的格式为列表
# nodes = '磁悬浮列车/上海宾家国际青年旅舍/苏州/南京路步行街/豫园/南园/上海环球金融中心/外滩'.split('/')
# DG.add_nodes_from(nodes)
#添加边，数据格式为列表
# for i in range( len( nodes )-1 ):
#     DG.add_edge( 'A', )
    # DG.add_weighted_edges_from([('田子坊', '迪士尼',5), ('田子坊', '城隍庙',4.5), ('田子坊', '外滩',3)])
# DG.add_edges_from()
#作图，设置节点名显示,节点大小，节点颜色
DG.add_edge('A','c',weight=0.6)
DG.add_edge('A','e',weight=0.1)
nx.draw(DG,pos=nx.spring_layout(DG),with_labels=True, node_size=900)#, node_color = colors
plt.show()