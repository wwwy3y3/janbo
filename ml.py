# -*- coding: utf-8 -*-
import pprint, collections
from itertools import *
pp = pprint.PrettyPrinter(indent=4)
def count_like(num, train):
    klass= [ train[i][10] for i in range(0,len(train)) ]#171 = num of train
    xv= [ train[i][num] for i in range(0,len(train)) ]
    counts= [ [0.0]*10 for i in range(0,7) ]


    # compare
    for pair in izip(klass, xv):
        #print int(pair[0]),int(pair[1])
        counts[int(pair[0])-1][int(pair[1])-1] += 1
    return counts

# open file
glass = open("glass.data", "r")

# 初始化資料矩陣
list_glass=[ map(float, line.rstrip('\n').split(',')) for line in glass ]

# 萃取每個attribute 成一個新的矩陣
reverse= []

for i, row in enumerate(list_glass):
    sliced= row
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

# start to do discretization
import math
for i in range(1,10): #attribute 1 to 9 need to discretizize
    minimun = min(reverse[i])
    maximun = max(reverse[i])
    width = (maximun-minimun)/10 # 10 bins
    for j in range(0,len(list_glass)): #214 = num of instance in data
        if reverse[i][j] == maximun:
            reverse[i][j] = 10
        else:
            reverse[i][j] = math.floor((reverse[i][j] - minimun) / width) + 1

#add k-fold attribute
import  random
reverse.append(random.sample(range(0,len(list_glass)),len(list_glass)))
width = 43  #43 43 43 43 42 has the nearset variance
for j in range(0,len(list_glass)): #discretize to 5 interval
        reverse[11][j] = math.floor((reverse[11][j] - minimun) / width) + 1 

# reverse the list again (discretization + group index) become 12 attrbutes
new_glass = []
for i, row in enumerate(reverse):
    sliced= row
    for x, val in enumerate(sliced):
        if(len(new_glass) > x):
            new_glass[x].append(sliced[x])
        else:
            new_glass.append([])
            new_glass[x].append(sliced[x])


#do k-fold
test = []
train = []
for i in range(0,len(list_glass)):
    if int(new_glass[i][11]) == 1: # set fold one as testing data !!REMENBER ADD LOOP
        test.append(new_glass[i])
    else:
        train.append(new_glass[i])
#calcualte the number of each class
count_class = []
for i in range(1,8): # the possible value class
    count = 0.0
    for j in range(0,len(train)): #171 is the number of train
        if i == train[j][10]:
            count += 1
    count_class.append(count)
print count_class

#cumulate
count_likes= [count_like(num, train) for num in xrange(1,10)]
'''pp.pprint(count_likes)'''
#predict the class of test
corrects = [] #of correct for each attribute
for k in range(1,10):#attribute1 to 9 
    predict_class =[] # predict class value for test 
    for i in range(0,len(test)):
        v = int(test[i][k]) #use the attribute1 as example
        posteriors = [] # posterior for each class
        for j in range(1,8): #class 1 to 7
            prior = count_class[j-1]/float(len(test))
            likelihood = (count_likes[0][j-1][v-1]+1)/(count_class[j-1]+10)
            posterior = prior*likelihood
            posteriors.append(posterior)
        #print posteriors 
        for j in range(1,8): #class 1 to 7
            if posteriors[j-1] == max(posteriors):
                predict_class.append(j)
    correct = 0
    for i in range(0,len(test)):
        if predict_class[i] == int(test[i][10]):
            correct += 1
    corrects.append(correct)
print "corrects = ",corrects
# select attribute
select_attributes = []
accuracies = []
for i in range(0,len(corrects)):#find which attribute should be selected
    if corrects[i] == max(corrects):
        select_attribute = i+1
        select_attributes.append(select_attribute)
        accuracy = corrects[i]/float(len(test))
        accuracies.append(accuracy)
        break #avoid pick up two attribute in once, beacuse they have same accuracy
print "attribute = ",select_attributes, "accuracy = ", accuracies









