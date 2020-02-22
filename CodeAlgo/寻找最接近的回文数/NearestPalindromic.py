# -*- coding: utf-8 -*-


def NearestPalindromic(n):
    '''
    寻找最接近的回文数
    给定一个由字符串表示的正整数n，找到与它最近的回文数（不包括自身）
    “最近的”定义为两个整数差的绝对值最小
    https://leetcode-cn.com/problems/find-the-closest-palindrome/
    
    思路：保留高位数字，改变低位数字，利用前半部分n_left（高位数）做镜像生成回文数
         值最接近的回文数可能为n_left、n_left+1或n_left-1产生的回文数，三者比较即可
         特殊情况单独处理
         截取n_left时分n的长度为奇数和偶数两种情况
	参考：
		https://leetcode-cn.com/problems/find-the-closest-palindrome/solution/zhao-gui-lu-by-heng-29/
		https://leetcode-cn.com/problems/find-the-closest-palindrome/solution/jing-xiang-dui-bi-by-dui-fang-xian-ru-chen-si/
    '''
    
    try:
        n_int = int(n)
        if n_int < 0:
            print('n小于0！')
            return None
    except:
        print('输入n应为字符串表示的正整数！')
        return None
    
    lenn = len(n)
    lenn_half = lenn // 2
    
    # 特殊情况：只有一位数
    if lenn_half == 0:
        return '1' if n == '0' else str(n_int-1)
    
    # 特殊情况：开头1，中间若干个0，末尾一个数字
    if n[0] == '1' and not any([int(x) for x in n[1:-1]]):
        # 若最后一位为0或1，结果应全由9构成；若最后一位为其他，则将最后一位改为1即可
        if n[-1] in ['0', '1']:
            return '9' * (lenn-1)
        else:
            return n[:-1] + '1'
        
    # 特殊情况：全是9
    if not any([int(x)-9 for x in n]):
        return str(n_int+2)
    
    # n为偶数位
    if lenn % 2 == 0:
        n_left = n[:lenn_half]
        tgt_n = n_left + n_left[::-1] # 原数反转
        tmp = str(int(n_left)-1)
        tgt_sml = tmp + tmp[::-1] # 小的目标值
        tmp = str(int(n_left)+1)
        tgt_big = tmp + tmp[::-1] # 大的目标值
    else:
        n_left = n[:lenn_half]
        tgt_n = n_left + n[lenn_half] + n_left[::-1]
        tmp = str(int(n[:lenn_half+1])-1)
        tgt_sml = tmp + tmp[:-1][::-1]
        tmp = str(int(n[:lenn_half+1])+1)
        tgt_big = tmp + tmp[:-1][::-1]
        
    # 从大到小排除其他两个结果
    ans = tgt_big
    for t in [tgt_n, tgt_sml]:
        dif = abs(int(t)-n_int)
        if dif > 0 and dif <= abs(int(ans)-n_int):
            ans = t
            
    return ans


if __name__ == '__main__':
    n = '123'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '1234'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '1'
    print(n+': ——>', NearestPalindromic(n))

    n = '10'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '102'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '100'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '600'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '198'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '598'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '101'
    print(n+': ——>', NearestPalindromic(n))
    
    n = 'abc'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '-102'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '22'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '11'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '1002'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '1000'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '88'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '11911'
    print(n+': ——>', NearestPalindromic(n))
    
    n = '1283'
    print(n+': ——>', NearestPalindromic(n))
    