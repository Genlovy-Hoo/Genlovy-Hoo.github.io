# -*- coding: utf-8 -*-

import re


def StrongPasswordChecker(s):
    '''
    强密码检测器
    https://leetcode-cn.com/problems/strong-password-checker/
    一个强密码应满足3个条件：
        1）由至少6个，至多20个字符组成；
        2）至少包含一个小写字母，一个大写字母，和一个数字；
        3）同一字符不能连续出现三次 (比如'.aaa.'不可以，但'.aa.a.'是可以的)。
    编写函数StrongPasswordChecker(s)，s代表输入字符串，要求实现：
        如果s已经符合强密码条件，则返回0；
        否则返回要将s修改为满足强密码条件的字符串所需要进行修改的最小步数
        （插入、删除、替换任一字符都算作一次替换）。
        
    思路:
        如果缺失类型有Nmis种，则至少进行Nmis次操作（插入或替换），故Nmis为操作次数下界。
        
        如果长L度小于6，那么通过添加6-L个字符使密码合法（因为最长长度是5，添加一个字符就可以
        打破连续三字符，所以不需要考虑连续），结果应为max(6-L, Nmis)。
        
        如果L小于等于20，那么通过替换进行去连续。一个长度为X的连续串，需要X//3次替换
        （或X//2次插入或X-2次删除，所以不考虑插入和删除操作）。记替换次数为Nrep，
        结果应为max(Nrep, Nmis)。
        
        如果L大于20，必须进行Ndel = L-20次删除操作，删除后还需要替换去除连续。
        结果应为Ndel + max(Nrep, Nmis)。
        在删除的时候应尽量删除连续字符以减少后续替换的数量。
        连续子串的长度不一定是某个固定模式的：
            如果连续串长度是3n的形式，那么先删除1个字符，可以减少一次替换操作。
            如果连续串长度是3n+1的形式，那么先删除2个字符，可以减少一次替换操作。
            如果连续串长度是3n+2的形式，那么先删除3个字符，可以减少一次替换操作。
            可先将长度为3n和3n+1形式的重复子串进行删除操作，统一转化为3n+2形式。
            
            假设长度为3n形式的子串有del1个，可全部先删除一个字符，共减少del1次替换操作，
            Nrep变为Nrep - min(Ndel, del1)。            
            
            假设长度为3n+1形式的子串有del2个，有必要先删除2个字符从而减少后续一次替换操作
            的子串个数应为min((Ndel-del1) // 2, del2)个（注：不一定所有的子串都需要
            进行先删除2个字符，比如'Aa0abcdefghiooookoooo'，只需要替换不需要删除），
            从而Nrep变为Nrep - min((Ndel-del1) // 2, del2)。
            
            经过前两种情况的处理之后，所有需要删除的点中重复子串长度全部转化为3n+2形式。
            剩余删除点个数为Ndel-del1-2*del2，由于每删除3个点可以减少一次替换操作，
            故最多可减少的替换操作次数为(Ndel-del1-2*del2) // 3，
            从而Nrep变为Nrep - (Ndel-del1-2*del2) // 3。
            
    参考:
        https://leetcode-cn.com/problems/strong-password-checker/solution/shi-jian-onkong-jian-o10mssi-lu-by-jriver/
        https://leetcode-cn.com/problems/strong-password-checker/solution/si-lu-qing-xi-ban-yun-ban-ben-by-bakezq/
    '''
    
    if not isinstance(s, str):
        print('s必须为字符串！')
        return None
    
    L = len(s)
    
    # Nmis: 缺失类型数
    mis_a = 0 if re.search('[a-z]+', s) else 1
    mis_A = 0 if re.search('[A-Z]+', s) else 1
    mis_d = 0 if re.search('\d+', s) else 1
    Nmis = mis_a + mis_A + mis_d
    
    del1, del2, Nrep = 0, 0, 0
    i = 2
    while i < L:
        # 若单个字符的最大重复次数超过3
        if s[i] == s[i-1] and s[i-1] == s[i-2]:
            # X记录最大重复次数
            X = 3            
            while i+1 < L and s[i+1] == s[i]:
                i += 1
                X += 1
            
            Nrep += X // 3 # 对重复字符串进行替换需要操作次数
            
            if X % 3 == 0:
                # 当重复次数为3n(n >= 1)，提前删除一个字符可减少一次替换操作
                del1 += 1
            elif X % 3 == 1:
                # 当重复次数为3n+1(n >= 1)，提前删除两个字符可减少一次替换操作
                del2 += 1
            
        i += 1
            
    if L < 6:
        # 当长度小于6时，不需要进行替换和删除操作，只需在适当位置插入缺失类型字符即可
        # （若有重复长度大于3的，只需要在中间插入打断其重复长度即可，如'aaaaa'—>'aaAaa0'）
        return max(6-L, Nmis)
    elif L <= 20:
        # 当长度在20及以内时，由于删除和插入的效率小于等于替换，且效果相同，故不考虑删除操作
        # 缺失类型的插入操作均可用替换操作代替
        return max(Nrep, Nmis)
    else:
        Ndel = L-20 # 必须要进行的删除次数
        Nrep -= min(Ndel, del1) # 提前删除一个字符代替（减少）一次替换
        # 提前删除2个字符代替（减少）一次替换操作
        if Ndel - del1 > 0:
            Nrep -= min((Ndel-del1) // 2, del2)
        # 提前删除3个字符代替（减少）一次替换操作
        if Ndel-del1-2*del2 > 0:
            Nrep -= (Ndel-del1-2*del2) // 3
        return Ndel + max(Nrep, Nmis)
        

if __name__ == '__main__':
    s = 'AAabc3'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = 'aaaaa'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s='AAVAaBCD222'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = ''
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = '1111111111'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = 'aaaaabbbb1234567890ABA'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = '1234567890123456Baaaaa'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = 'Aa0abcdefghijkooooooo'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s='Aa0abcdefghiooookoooo'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s='Aa0abcdefghhhhhijjjjj'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s='Aa0abbbbbghhhhhijjjjj'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s='Aa0abbbbbghhhhhijjjjjxy'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = 'aaaaaa1234567890123Ubefg'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = 'aaaaaaa1234567890123Ucd'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = 'Aa0abcdefghiooookoooooooooo'
    print(s+':')
    print(StrongPasswordChecker(s))
    
    s = 567
    print(StrongPasswordChecker(s))
    
