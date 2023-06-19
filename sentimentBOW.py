import sys
import csv
import os

file1 = open(sys.argv[1])
f1 = file1.readlines()
file2 = open(sys.argv[2])
f2 = file2.readlines()
thresh = int(sys.argv[3])
file_name1 = os.path.splitext(sys.argv[1])[0] + "_BOW" + str(thresh) +  ".csv"
file_name2 = os.path.splitext(sys.argv[2])[0] + "_BOW" + str(thresh) + ".csv"
op1 = open(file_name1, 'w')
op2 = open(file_name2, 'w')


def islabel(s, i, arr):
    if i == 0:
        return True
    if s == "0" or s == "1":
        if arr[i-1] == '\n' or arr[i-1] == '':
            return True
    return False


for i in range(0,len(f1)):
    f1[i] = f1[i].replace('\n', '')
for i in range(0,len(f2)):
    f2[i] = f2[i].replace('\n', '')


def freqcount(s):
    count = 0
    for word in f1:
        if s == word:
            count = count +1
    if count >= thresh:
        return count
    else: return -1


def search(s):
    for word_pair in lex:
        if s == word_pair[0]:
            return word_pair[1]
    return -1


def searchin(s):
    for i in range(len(lex)):
        if s == lex[i][0]:
            return i
    return -1

lex = []
for i in range(len(f1)):
    if f1[i] != '1' and f1[i]!= '0' and f1[i] != '' and f1[i] != '\n':
        if search(f1[i]) == -1:
            if freqcount(f1[i]) != -1:
                lex.append([f1[i],freqcount(f1[i])])


def bubbleSort(arr):
    n = len(arr)
    swapped = False
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j][1] < arr[j + 1][1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            if arr[j][1] == arr[j+1][1]:
                if arr[j][0] > arr[j+1][0]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        if not swapped:
            return


bubbleSort(lex)
header = ['LABEL']
for i in range(len(lex)):
    s = "F" + str(i)
    header.append(s)

writer = csv.writer(op1)
writer.writerow(header)
writer = csv.writer(op2)
writer.writerow(header)
f1mod = []
i = 0
while i < len(f1):
    if islabel(f1[i],i,f1):
        str = f1[i] + '@'
        i = i+1
        while i < len(f1) and not islabel(f1[i],i,f1) :
            #print(i)
            if f1[i] != '':
                if f1[i] == ',':
                    str = str + "," + '@'
                else:
                    str = str + f1[i] + '@'
            i = i+1
    f1mod.append(str)
for i in range(0, len(f1mod)):
    f1mod[i] = f1mod[i].split('@')


def featurevec(vec):
    arr = []
    arr.append(int(vec[0]))
    for i in range(len(lex)):
        arr.append(0)
    for i in range(1,len(vec)):
        if search(vec[i]) != -1:
            count = 0
            for j in range(1,len(vec)):
                if vec[j] == vec[i]:
                    count = count +1
            arr[searchin(vec[i])+1] = count
    return arr


writer = csv.writer(op1)
for i in range(len(f1mod)):
    writer.writerow(featurevec(f1mod[i]))


f2mod = []
i = 0
while i < len(f2):
    if f2[i] == '1' or f2[i] == '0':
        str = f2[i] + '@'
        i = i+1
        while i < len(f2) and f2[i] != '1' and f2[i] != '0':
            #print(i)
            if f2[i] != '':
                if f2[i] == ',':
                    str = str + "," + '@'
                else:
                    str = str + f2[i] + '@'
            i = i+1
    f2mod.append(str)
for i in range(0, len(f2mod)):
    f2mod[i] = f2mod[i].split('@')

writer = csv.writer(op2)
for i in range(len(f2mod)):
    writer.writerow(featurevec(f2mod[i]))
