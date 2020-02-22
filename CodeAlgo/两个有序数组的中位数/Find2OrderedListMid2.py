# -*- coding: utf-8 -*-


def Find2OrderedListMid(nums1, nums2): 
    '''
    给定两个有序数组（升序）列表nums1和nums2，求两个列表合并之后的中位数
    https://leetcode-cn.com/problems/median-of-two-sorted-arrays/
    
    复杂度: O(log(n1+n2))，n1和n2分为别数组长度
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
    if n1 == 0 or n2 == 0:
        nums = nums1 + nums2
        mid = get_ordered_mid(nums, N_left, odd)
        return mid
    
        
    idx1 = n1-1    
    idx2 = N_left - (idx1+1)  
    
    # 注意这里idx2的最大取值为n2-1，原因在于限制了n1 <= n2
    while nums1[idx1] > nums2[idx2] and idx1 > -1 and idx2 < n2-1:
        idx1 -= 1
        idx2 += 1
        
    nums1_left = nums1[0:idx1+1]
    nums1_right = nums1[idx1+1:]
    nums2_left = nums2[0:idx2]
    nums2_right = nums2[idx2:]
      
    if odd:           
        mid = min(nums1_right + nums2_right) 
    else:
        max_left = max(nums1_left + nums2_left)
        min_right = min(nums1_right + nums2_right)
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
    