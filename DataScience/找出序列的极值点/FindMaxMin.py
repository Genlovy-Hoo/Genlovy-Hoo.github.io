# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt


def plot_MaxMins(data, col, col_label, idx1=None, idx2=None,
                 label_legend=['Max', 'Min'], figsize=(11, 6), title=None,
                 markersize=10, fontsize=20, fig_save_path=None):
    '''
    绘制序列数据（data[col指定列]）并标注极大极小值点，idx1和idx2指定绘图用数据起止位置
    data必须包含列: [col指定列, col_label指定列]
    col_label指定列中值1表示极大值点，-1表示极小值点，0表示普通点
    label_legend指定col_label为1和-1时的图标标注
    '''
    
    N = data.shape[0]
    if all([idx1, idx2]) and idx2 - idx1 <= 2:
        idx1, idx2 = 0, N
    idx1 = 0 if idx1 is None or idx1 < 0 or idx1 > N-2 else idx1
    idx2 = N if idx2 is None or idx2 > N or idx2 < 2 else idx2
    df = data.iloc[idx1:idx2, :].copy()
    if df.index.name is None:
        df.index.name = 'idx'        
    idx_name = df.index.name
    if idx_name in df.columns:
        df.drop(idx_name, axis=1, inplace=True)
    df.reset_index(inplace=True)
    
    series = df[col]
    series_max = df[df[col_label] == 1][col]
    series_min = df[df[col_label] == -1][col]
    
    plt.figure(figsize=figsize)
    plt.plot(series, '-k.', label=col)
    plt.plot(series_max, 'bv', markersize=markersize, label=label_legend[0])   
    plt.plot(series_min, 'r^', markersize=markersize, label=label_legend[1])
    plt.legend(loc=0, fontsize=fontsize)    
    
    n = idx2 - idx1
    xpos = [int(x*n/8) for x in range(0, 8)] + [n-1]
    plt.xticks(xpos, [df.loc[x, idx_name] for x in xpos])
    plt.grid()
    
    if title:
        plt.title(title, fontsize=fontsize)
        
    if fig_save_path:
        plt.savefig(fig_save_path)
        
    plt.show()
    
    
def con_count(series, Fcond):
    '''
    计算series(pd.Series)中连续满足Fcond函数指定的条件的记录数
    Fcond为函数，Fcond(x)返回结果只能为True或False
    返回pd.DataFrame，包含原始series列和连续满足条件计数的count列
    
    eg.
        series = pd.Series([0, 1, 1, 0, 0, 1, 1, 1])
        Fcond = lambda x: True if x == 1 else False
        con_count(series, Fcond):
               series  count
            0       0      0
            1       1      1
            2       1      2
            3       0      0
            4       0      0
            5       1      1
            6       1      2
            7       1      3
    '''
    
    if series.name is None:
        series.name = 'series'
    col = series.name    
    df = pd.DataFrame(series)
    
    df['count'] = 0
    k = 0
    while k < df.shape[0]:
        if Fcond(df.loc[df.index[k], col]):
            count = 1
            df.loc[df.index[k], 'count'] = count
            ktmp = k + 1
            while ktmp < df.shape[0] and Fcond(df.loc[df.index[ktmp], col]):
                count += 1
                df.loc[df.index[ktmp], 'count'] = count
                ktmp += 1
            k = ktmp
        else:
            k += 1
            
    return df

    
def FindMaxMin(series, Tmin=2):
    '''
    寻找序列series的极值点
    
    Args:
        series: pd.Series，待寻找极值点的序列
        Tmin: 设置极大极小值之间至少需要间隔Tmin个点（相当于最小半周期）
    
    Return:
        Smax: 极大值点序列
        Smin: 极小值点序列
        df: 包含原始序列和'label'列，
            'label'列中1表示极大值点，-1表示极小值点，0表示普通点
    '''
    
    if len(series) < 2:
        raise ValueError('输入series长度不能小于2！')
        
    if not isinstance(series, pd.core.series.Series):
        series = pd.Series(series)
    
    # 序列名和索引名
    if series.name is None:
        series.name = 'series'
    if series.index.name is None:
        series.index.name = 'idx'
    
    df = pd.DataFrame(series)
    col = df.columns[0]
    df['dif'] = series.diff()
    
    # 极大值点
    df['dif_big'] = (df['dif'] > 0).astype(int)
    df['big_rep'] = df['dif_big'].cumsum()
    df['big_rep'] = df[df['dif_big'] == 0]['big_rep'].diff()
    df['big_rep'] = df['big_rep'].shift(-1).fillna(0)
    df.loc[df.index[0], 'big_rep'] = 1 if df['dif'].iloc[1] < 0 else 0
    df.loc[df.index[-1], 'big_rep'] = 1 if df['dif'].iloc[-1] > 0 else 0
    
    # 极小值点
    df['dif_sml'] = (df['dif'] < 0).astype(int)
    df['sml_rep'] = df['dif_sml'].cumsum()
    df['sml_rep'] = df[df['dif_sml'] == 0]['sml_rep'].diff()
    df['sml_rep'] = df['sml_rep'].shift(-1).fillna(0)
    df.loc[df.index[0], 'sml_rep'] = 1 if df['dif'].iloc[1] > 0 else 0
    df.loc[df.index[-1], 'sml_rep'] = 1 if df['dif'].iloc[-1] < 0 else 0
    
    df['label'] = df[['big_rep', 'sml_rep']].apply( lambda x:
        1 if x['big_rep'] > 0 else (-1 if x['sml_rep'] > 0 else 0), axis=1)
    
    df.reset_index(inplace=True)
        
    # 保证极大极小值必须是间隔的，不能连续出现极大值或连续出现极小值
    # 注：如果序列中存在相邻的值相等，则按上面方法可能可能出现连续的极大/小值点
    k = 0
    while k < df.shape[0]:
        if df.loc[k, 'label'] == 0:
            k += 1
        elif df.loc[k, 'label'] == -1:
            k1 = k
            idxs = [] # 连续极小值点索引列表
            while k1 < df.shape[0] and df.loc[k1, 'label'] != 1:
                if df.loc[k1, 'label'] == -1:
                    idxs.append(k1)
                k1 += 1
            if len(idxs) > 1:
                for n in idxs:
                    # 保留最小的极小值点（不可能出现值相等的连续极大/小值点）
                    if df.loc[n, col] == df.loc[idxs, col].min():
                        df.loc[n, 'label'] == -1
                    else:
                        df.loc[n, 'label'] = 0
            k = k1
        else:
            k1 = k
            idxs = [] # 连续极大值点索引列表
            while k1 < df.shape[0] and df.loc[k1, 'label'] != -1:
                if df.loc[k1, 'label'] == 1:
                    idxs.append(k1)
                k1 += 1
            if len(idxs) > 1:
                for n in idxs:
                    # 保留最大的极大值点（不可能出现值相等的连续极大/小值点）
                    if df.loc[n, col] == df.loc[idxs, col].max():
                        df.loc[n, 'label'] == 1
                    else:
                        df.loc[n, 'label'] = 0
            k = k1
    
    # Tmin应大于等于1
    if Tmin is not None and Tmin < 1:
        Tmin = None
    
    if Tmin:
        def del_Tmin(df):
            '''
            删除不满足最小半周期的极值点对（由一个极大一个极小两个极值点组成），删除条件：
                1：间隔小于Tmin
                2：删除后不影响趋势拐点
            注：df中数据的排序依据为df.index
            '''
            
            k2 = 0
            while k2 < df.shape[0]:
                if df.loc[k2, 'label'] == 0:
                    k2 += 1
                else:
                    k1 = k2-1
                    while k1 > -1 and df.loc[k1, 'label'] == 0:
                        k1 -= 1
                        
                    k3 = k2+1
                    while k3 < df.shape[0] and df.loc[k3, 'label'] == 0:
                        k3 += 1 
                        
                    k4 = k3 +1
                    while k4 < df.shape[0] and df.loc[k4, 'label'] == 0:
                        k4 += 1
                       
                    # 删除条件1
                    if k3-k2 < Tmin+1 and k4 < df.shape[0] and k1 > -1:
                        if df.loc[k2, 'label'] == 1:
                            # 删除条件2
                            if df.loc[k2, col] <= df.loc[k4, col] and \
                                           df.loc[k3, col] >= df.loc[k1, col]:
                                df.loc[[k2, k3], 'label'] = 0
                                
                        else:
                            # 删除条件2
                            if df.loc[k2, col] >= df.loc[k4, col] and \
                                           df.loc[k3, col] <= df.loc[k1, col]:
                                df.loc[[k2, k3], 'label'] = 0
                            
                    # 开头部分特殊处理
                    elif k3-k2 < Tmin+1 and k4 < df.shape[0] and k1 < 0:
                        if df.loc[k2, 'label'] == 1 and \
                                        df.loc[k2, col] < df.loc[k4, col]:
                            df.loc[k2, 'label'] = 0
                        if df.loc[k2, 'label'] == -1 and \
                                        df.loc[k2, col] > df.loc[k4, col]:
                            df.loc[k2, 'label'] = 0
                            
                    k2 = k3
                
            return df
        
        df = del_Tmin(df)        
        
        df.index = range(df.shape[0]-1, -1, -1)
        df = del_Tmin(df)
        
        def check_Tmin(df, Tmin):
            Fcond = lambda x: True if x == 0 else False
            df['tmp'] = con_count(df['label'], Fcond)['count'].shift(1)
            df['tmp'] = abs(df['tmp'] * df['label'])
            df.loc[df.index[0], 'tmp'] = 0
            tmp = list(df[df['label'] != 0]['tmp'])
            df.drop('tmp', axis=1, inplace=True)
            if len(tmp) <= 3:
                return True, tmp
            else:
                tmp = tmp[1:]
                if all([x >= Tmin for x in tmp]):
                    return True, tmp
                else:
                    return False, tmp
        TminOK, tmp = check_Tmin(df, Tmin)
        tmp_new = []
#        plot_MaxMins(df, col, 'label', title='Tmin check: '+str(TminOK))
        # 注：特殊情况下不可能满足任何两个极大极小值对之间的间隔都大于Tmin
        while not TminOK and not tmp == tmp_new:
            TminOK, tmp = check_Tmin(df, Tmin)
            df.index = range(df.shape[0])
            df = del_Tmin(df)
            df.index = range(df.shape[0]-1, -1, -1)
            df = del_Tmin(df)
            TminOK, tmp_new = check_Tmin(df, Tmin)
#            plot_MaxMins(df, col, 'label', title='Tmin check: '+str(TminOK))
        
    df.set_index(series.index.name, inplace=True)
            
    Smax = df[df['label'] == 1][col]
    Smin = df[df['label'] == -1][col]
        
    return Smax, Smin, df.reindex(columns=[col, 'label'])


def check_peaks(df, col, col_label):
    '''
    检查df中col_label指定列的极值点排列是否正确
    要求df须包含指定的两列，其中：
        col_label指定列保存极值点，1表示极大值，-1表示极小值，0表示普通点
        另一列为序列数值列
    '''
        
    tmp = df.reset_index()
    df_part = tmp[tmp[col_label].isin([1, -1])]
    
    # 不能出现连续的极大/极小值点
    label_diff = list(df_part[col_label].diff().unique())
    if 0 in label_diff:
        return False, '存在连续极大/极小值点'
    
    # 极大/小值点必须大/小于极小/大值点
    for k in range(1, df_part.shape[0]-1):
        if df_part[col_label].iloc[k] == 1:
            if df_part[col].iloc[k] <= df_part[col].iloc[k-1] or \
                            df_part[col].iloc[k] <= df_part[col].iloc[k+1]:
                return False, ('极大值点小于等于极小值点',
                               df.index[df_part.index[k]])
        else:
            if df_part[col].iloc[k] >= df_part[col].iloc[k-1] or \
                            df_part[col].iloc[k] >= df_part[col].iloc[k+1]:
                return False, ('极小值点大于等于极大值点',
                               df.index[df_part.index[k]])
    
    # 极大极小值点必须是闭区间内的最大最小值
    for k in range(0, df_part.shape[0]-1):
        idx1 = df_part.index[k]
        idx2 = df_part.index[k+1]
        if tmp.loc[idx1, col_label] == 1:
            if tmp.loc[idx1, col] != tmp.loc[idx1:idx2, col].max() or \
                    tmp.loc[idx2, col] != tmp.loc[idx1:idx2, col].min():
                return False, ('极大极小值不是闭区间内的最大最小值',
                               [df.index[idx1], df.index[idx2]])
        else:
            if tmp.loc[idx1, col] != tmp.loc[idx1:idx2, col].min() or \
                    tmp.loc[idx2, col] != tmp.loc[idx1:idx2, col].max():
                return False, ('极大极小值不是闭区间内的最大最小值',
                               [df.index[idx1], df.index[idx2]])
            
    return True, None


if __name__ == '__main__':
    # 二次曲线叠加正弦余弦-------------------------------------------------------
    N = 200
    t = np.linspace(0, 1, N)
    s = 6*t*t + np.cos(10*2*np.pi*t*t) + np.sin(6*2*np.pi*t)
    s = pd.Series(s)
    
#    Tmin = None
    Tmin = 20
    s_max, s_min, df = FindMaxMin(s, Tmin=Tmin)
    
    plot_MaxMins(df, 'series', 'label', 
                 title='寻找极大极小值test：Tmin='+str(Tmin))
    
    OK, e = check_peaks(df, df.columns[0], df.columns[1])
    if OK:
        print('极值点排列正确！')
    else:
        print('极值点排列错误:', e)
        
