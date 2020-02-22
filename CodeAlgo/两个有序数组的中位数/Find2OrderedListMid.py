# -*- coding: utf-8 -*-


def Find2OrderedListMid(nums1, nums2): 
    '''
    给定两个有序数组（升序）列表nums1和nums2，求两个列表合并之后的中位数
    https://leetcode-cn.com/problems/median-of-two-sorted-arrays/
    
    复杂度: O(log(n1+n2))，n1和n2分为别数组长度
    相对于Find2OrderedListMid2.py，这里不使用中间变量nums，从而更节省空间
    '''
    
    if not isinstance(nums1, list) or not isinstance(nums2, list):
        print('请输入两个列表！')
        return None
    
      
    n1, n2 = len(nums1), len(nums2)
    N = n1 + n2
    N_left = int(N/2) # 合并数列中，中位数前面的数的个数
    odd = False if N % 2 == 0 else True
    
    
    if N == 0:
        print('两个数组的长度均为0！')
        return None
    
    
    # 保持nums1的长度小于等于nums2
    if n1 > n2:
        nums1, nums2 = nums2, nums1
        n1, n2 = len(nums1), len(nums2)
    
        
    def get_ordered_mid(nums, N_left, odd):
        if odd:
            return nums[N_left]
        else:
            return (nums[N_left-1] + nums[N_left]) / 2
            
            
    # 若其中一个为空列表，直接获取中位数
    if n1 == 0:
        mid = get_ordered_mid(nums2, N_left, odd)
        return mid
    
    if n2 == 0:
        mid = get_ordered_mid(nums1, N_left, odd)
        return mid
    
        
    idx1 = n1-1    
    idx2 = N_left - (idx1+1)  
    
    # 注意这里idx2的最大取值为n2-1，原因在于限制了n1 <= n2
    while nums1[idx1] > nums2[idx2] and idx1 > -1 and idx2 < n2-1:
        idx1 -= 1
        idx2 += 1
      
    if odd:    
        # odd为True时有两种情况：nums1的数全分配到左边或左右都有
        # (由于odd为True时必有n1<n2，因此nums2的数不可能全部分配到左边)
        if idx1 == n1-1: # nums1的数全分配到左边
            mid = nums2[idx2]
        else:
            mid = min(nums1[idx1+1], nums2[idx2])
    else:
        # odd为False时计算左边部分最大值，有三种情况
        if idx1 == -1: # nums1的数全部分配到右边
            max_left = nums2[idx2-1]
        elif idx2 == 0: # nums2的数全部分配到右边
            max_left = nums1[idx1]
        else:
            max_left = max(nums1[idx1], nums2[idx2-1])
        
        # odd为False时计算右边最小值，有两种情况
        # （由于N为偶数且n1 <= n2，因此当nums2的数全部分配到左边时，实际上n1 == n2，
        #  计算中位数时也要取nums2最后一个值）
        if idx1 == n1-1: # nums1的数全分配到左边
            min_right = nums2[idx2]
        else:
            min_right = min(nums1[idx1+1], nums2[idx2])
            
        mid = (max_left + min_right) / 2
                   
    return mid
    
    
if __name__ == '__main__':
    nums1 = [1, 2, 3, 4]
    nums2 = [2, 6, 7, 8, 9]
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [1, 3, 5, 9]
    nums2 = [2, 4, 6, 7, 9, 10, 11]    
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [1, 2]
    nums2 = [3, 4]    
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = []
    nums2 = [1]    
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = []
    nums2 = [2, 3]    
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [3]
    nums2 = [-2, -1]    
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [4]
    nums2 = [1, 2, 3]    
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [1, 2]
    nums2 = [-1, 3]    
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [2]
    nums2 = [1, 3, 4]    
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [1, 3, 4]
    nums2 = [2]
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [3]
    nums2 = [1, 2, 4]
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [1, 4]
    nums2 = [2, 3]
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [4]
    nums2 = [1, 2, 3, 5]
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [2]
    nums2 = [1]
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [4, 5]
    nums2 = [1, 2, 3]
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = None
    nums2 = [1, 2, 3, 5]
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = []
    nums2 = []
    print(Find2OrderedListMid(nums1, nums2))
    
    nums1 = [1, 3, 5, 7, 9]
    nums2 = [2, 4, 6, 8, 10, 11]
    print(Find2OrderedListMid(nums1, nums2))
    