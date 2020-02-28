# -*- coding: utf-8 -*-


def FindAddends_BigFirst(M, alts, tol=0.0, max_loop=1000000): 
    '''
    从给定的列表alts（可以有负数）中选取若干个数，使其和最接近M
    
    思路: 大的备选数优先，从大到小依次加入备选数
         若加入新值之后找不到理想解，则删除最后加入的值，继续添加下一个更小的备选数
         下一个备选数确定方式：
             当alts中只有正数时，剩下的数中与剩余和（目标和减去当前和）最接近的数
             当alts中有负数时，直接取比最后加进去的数更小的数（搜索速度会变慢很多）
    
    Args:
        M: 目标和
        alts: list，备选数列表
        max_loop: 搜索次数限制
        
    Returns:
        choseds_best: list，最优备选数列表
    '''
    
    alts.sort() # 升序（大的数优先进入）
    all_postive = all([x >= 0 for x in alts])
    
    # 初始化
    # idx_last记录最新进入的数的索引号
    # chosed_idxs记录备选中的数的索引号
    # chosed_addends保存被选中的数
    # choseds_best保存最优结果
    # now_sum为chosed_addends求和
    idx_last = len(alts) - 1
    chosed_idxs = [idx_last]
    chosed_addends = [alts[idx_last]]
    choseds_best = []
    now_sum = alts[idx_last]
    
    # 搜索过程
    loop_count = 0
    while loop_count < max_loop:
        loop_count += 1
        
        # 更新最优解
        if abs(M - now_sum) < abs(M - sum(choseds_best)):
            choseds_best = chosed_addends.copy()
        
        # 结束条件
        if M == now_sum:
            print('找到最优解，结束搜索。')
            break
        
        # 无最优解（搜索到最小值且只剩它一个备选数），结束搜索
        if idx_last == 0 and len(chosed_idxs) == 1:
            print('无最优解，结束搜索。')
            break
        
        # 刚好搜索到最小值且不是最优解，此时去掉最小值并更改最小值前面一个进去的值
        if idx_last == 0:
            idx_last = chosed_idxs[-2] - 1
            del chosed_idxs[-2:]
            chosed_idxs.append(idx_last)
            del chosed_addends[-2:]
            chosed_addends.append(alts[idx_last])
            now_sum = sum(chosed_addends)
            continue
        
        # 下一个备选数
        if not all_postive:
            idx_last -= 1
        else:
            idx_last = backfind_sml1st_idx(M-now_sum, alts[0:idx_last])
        
        # 保留最后一个加进去的数情况下找不到最优解，更改最后进去的那个数
        if idx_last < 0:
            idx_last = chosed_idxs[-1] - 1
            chosed_idxs[-1] = idx_last
            chosed_addends[-1] = alts[idx_last]
            now_sum = sum(chosed_addends)
            continue
        
        chosed_idxs.append(idx_last)
        chosed_addends.append(alts[idx_last])
        now_sum += alts[idx_last]
            
    return choseds_best


def backfind_sml1st_idx(M, alts):
    '''
    alts（已升序排列）从后往前搜索，返回第一个小于等于M的数的索引
    '''
    if len(alts) == 0:
        return -1    
    idx = len(alts) - 1
    while idx >= 1 and alts[idx] > M:
        idx -= 1
    return idx
    

if __name__ == '__main__':    
    alts = [22, 15, 14, 13, 7, 6.1, 5, 21.5, 100]
    M = 22 + 21 + 4.1
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    
    alts = [200, 107, 100, 99, 98, 6, 5, 3, -1, -20, -25]
    M = 100 + 6 - 25
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    
    alts = [100, -100, -105, -102, -25, -30, -1]
    M = -26
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    
    alts = [10, 9, 8, 7, 6, 5]
    M = 17
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    
    alts = [10, 9, 8, -7, -6, -5]
    M = 3
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    
    alts = [10, 7, 6, 3]
    M = 18
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    
    alts = [10, 7, 6, 3]
    M = 12
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    
    alts = [10, 9, 8, 7, 6, 5, 3]
    M = 14
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    
    alts = [10, 9, 8, 7, 6, 5]
    M = 22
    print(FindAddends_BigFirst(M, alts, max_loop=10000000))
    