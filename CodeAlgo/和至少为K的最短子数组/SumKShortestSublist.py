# -*- coding: utf-8 -*-

import collections


def SumKShortestSublist(A, K):
    '''
    寻找和至少为K的最短子数组: 非空列表A的最短的非空连续子数组的长度，该子数组的和至少为K
    https://leetcode-cn.com/problems/shortest-subarray-with-sum-at-least-k/
    
    题目转换：
    记P存放A的累计求和列表(P[x+1] = P[x] + A[x])
    找到在满足P[y]-P[x] >= K情况下使y-x最小的y-x
    
    官方解答思路：
       全局最优解：最终需要的结果
       特定最优解x：当y固定时，满足条件的最大x
    
       特定最优解x满足规律：
       当y固定的时候，若x2 > x1且P[x2] <= P[x1](相当于A[x1]和A[x2]之间有负数)
       则x1必然不是y对应的特定最优解，因为若x1可行，则x2也可行且比x1更优
       因此(在x递增的方向)寻找y的特定最优解时，若x1 < x2且P[x1] >= P[x2]，则x1可直接删除
    
       当x为多个y的特定最优解时的规律：
       对于任何y2 > y1，若x同时是y1和y2对应的特定最优解，则y1-x一定优于y2-x
       因此在y递增的方向寻找全局最优解时，若x是y的特定最优解，则后续不用再考虑x(因为y递增)
       
       用一个双端列队deq存放可能是特定最优解的下标x，然后求解分两个步骤，对A的每个元素A[y]：
           1. 首先y固定，删除deq中所有x < y且P[x] > P[y]的x
           2. 对deq中的从小到大的每个下标x，若x为y的特定最优解，则将其删除
    '''
    
    if not isinstance(A, list) or len(A) < 1:
        print('A须为非空列表！')
        return -1
    
    N = len(A)
    P = [0] # 存放累计和列表
    for a in A:
        P.append(P[-1] + a)

    best_ans = N+1 # best_ans记录全局最优解，N+1 is impossible    
    deq = collections.deque() # 双端列队deq存放可能是特定最优解的下标x
    for y, P_y in enumerate(P):
        
        # 当y固定时，删除d中所有x < y且P[x] > P[y]的x
        while deq and P_y <= P[deq[-1]]:
            deq.pop()

        # 若x是y的特定最优解，则后续不用再考虑x
        while deq and P_y - P[deq[0]] >= K:
            best_ans = min(best_ans, y-deq.popleft())

        deq.append(y)

    return best_ans if best_ans < N+1 else -1


if __name__ == '__main__':
    A = [1]
    K = 1
    print(SumKShortestSublist(A, K))
    
    A = [1, 2]
    K = 5
    print(SumKShortestSublist(A, K))    

    A = [2, 1, 2]
    K = 3
    print(SumKShortestSublist(A, K))
    
    A = [2, -1, 2]
    K = 3
    print(SumKShortestSublist(A, K))
    
    A = [84, -37, 32, 40, 95]
    K = 167
    print(SumKShortestSublist(A, K))

