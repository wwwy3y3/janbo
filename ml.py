# -*- coding: utf-8 -*-

# open file
glass = open("glass.data", "r")

# 初始化資料矩陣
list_glass=[ map(float, line.rstrip('\n').split(',')) for line in glass ]

# 萃取每個attribute 成一個新的矩陣
reverse= []

for i, row in enumerate(list_glass):
    sliced= row[1:-1]
    for x, val in enumerate(sliced):
        if(len(reverse)>x): # exist a list, just append
            reverse[x].append(sliced[x])
        else:
            # not exist a list
            # init and append
            reverse.append([])
            reverse[x].append(sliced[x])

# now reverse is a 反轉矩陣去頭去尾

# close file
glass.close()


