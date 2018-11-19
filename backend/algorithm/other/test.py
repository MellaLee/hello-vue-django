# 应该是当时做的单元测试

import sys
import Levenshtein

def find_lcsubstr(s1, s2):   
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]  #生成0矩阵，为方便后续计算，比字符串长度多了一列  
    mmax=0   #最长匹配的长度  
    p=0  #最长匹配对应在s1中的最后一位  
    for i in range(len(s1)):  
        for j in range(len(s2)):  
            if s1[i]==s2[j]:  
                m[i+1][j+1]=m[i][j]+1  
                if m[i+1][j+1]>mmax:  
                    mmax=m[i+1][j+1]  
                    p=i+1  
    #return s1[p-mmax:p],mmax   #返回最长子串及其长度  
    return mmax   #返回最长子串及其长度  

def similarUrlAgrs(str1, str2):
    lcs=find_lcsubstr(str1, str2)  
    ld=Levenshtein.distance(str1, str2)
    return (lcs / (ld + lcs)) 
  
if __name__ == '__main__':  
    args = sys.argv
    similar = similarUrlAgrs(args[1], args[2])
    print (similar, Levenshtein.ratio(args[1], args[2]), Levenshtein.distance(args[1], args[2]))  