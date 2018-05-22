import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

def handle(inner):
    path = "orgData.xls"
    df = pd.read_excel(path)

    buInd = df['室外温度(℃)'] >= 6550
    df.loc[buInd, '室外温度(℃)'] = df.loc[buInd, '室外温度(℃)'] - 6553.6

    #df.to_excel("outMy.xls", sheet_name="气候补偿数据")

    df = df.sort_values(by='室外温度(℃)')

    df['室外温度(℃)']
    df['室内温度(℃)']
    df['二次供温(℃)']

    #inner = 20

    p_out2er = np.polyfit(df['室外温度(℃)'], df['二次供温(℃)'], deg=4)
    p_in2er = np.polyfit(df['室内温度(℃)'], df['二次供温(℃)'], deg=2)

    deg_out2er = np.poly1d(p_out2er)
    deg_in2er = np.poly1d(p_in2er)

    xvalue = deg_out2er(df['室外温度(℃)']) * deg_in2er(inner)
    yvalue = np.sqrt(xvalue)

    plt.plot(df['室外温度(℃)'], yvalue, c='b')
    plt.text(df['室外温度(℃)'][300], yvalue[300] - 0.5, "室外温度%s(℃)时的曲线" % inner)

    # plt.ylim(np.min(yvalue)-0.05)
    # plt.plot([df['室外温度(℃)'][300],df['室外温度(℃)'][300]],[np.min(yvalue)-0.05,yvalue[300]],"b--")
    plt.xlabel('室外温度(℃)')
    plt.ylabel('二次供温(℃)')
    plt.show()
