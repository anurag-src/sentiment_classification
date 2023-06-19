import sys
import csv
import os

file1 = open(sys.argv[1])
f1 = file1.readlines()
file2 = open(sys.argv[2])
f2 = file2.readlines()
lex = open(sys.argv[3])
lex = lex.readlines()
file_name1 = os.path.splitext(sys.argv[1])[0] + "_features.csv"
file_name2 = os.path.splitext(sys.argv[2])[0] + "_features.csv"
op1 = open(file_name1, 'w')
op2 = open(file_name2, 'w')
header = ['LABEL', 'DIFF', 'EXCL', 'NEG', 'NGTNEG', 'NGTPOS', 'POS', 'W1', 'W2', 'W3', 'W4', 'W5']
writer = csv.writer(op1)
writer.writerow(header)
writer = csv.writer(op2)
writer.writerow(header)


def islabel(s, i, arr):
    if i == 0:
        return True
    if s == "0" or s == "1":
        if arr[i-1] == '\n' or arr[i-1] == '':
            return True
    return False


for i in range(0, len(lex)):
    if lex[i] != '\n':
        lex[i] = lex[i].split()
f1mod = []
for i in range(0,len(f1)):
    f1[i] = f1[i].replace('\n', '')
for i in range(0,len(f2)):
    f2[i] = f2[i].replace('\n', '')
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


def search(s):
    for word_pair in lex:
        if s == word_pair[0]:
            if word_pair[1] == 'POS':
                return True
            return -1

    # while i < len(lex):
    #     #print(lex[i])
    #     #print(i)
    #     if s == lex[i][0]:
    #         if lex[i][1] == 'POS':
    #             return True
    #         if lex[i][1] == 'NEG':
    #             return -1
    #     i = i+1


def isneg(s):
    if s == 'no' or s == 'not' or s == 'never' or s == 'isn’t' or s == 'wasn’t' or s == 'won’t':
        return True
    return False


def feature_vec(s):
    excl = 0
    pos = 0
    neg = 0
    ngtneg = 0
    ngtpos = 0
    vec = []
    vec.append(int(s[0]))
    for i in range(1, len(s)):
        if s[i] == '!':
            excl = excl + 1
        if search(s[i]) == True:
            pos = pos + 1
            j = i - 2
            while j < len(s) and j < i + 3:
                if isneg(s[j]):
                    ngtpos = ngtpos + 1
                j = j + 1

        if search(s[i]) == -1:
            neg = neg+1
            j = i - 2
            while j < len(s) and j < i + 3:
                if isneg(s[j]):
                    ngtneg = ngtneg + 1
                j = j + 1
    vec.append(pos-neg)
    vec.append(excl)
    vec.append(neg)
    vec.append(ngtneg)
    vec.append(ngtpos)
    vec.append(pos)
    for k in range(1,6):
        if k< len(s)-1:
            vec.append(s[k])
        if k>= len(s)-1:
            vec.append("UNK")
    return vec


writer = csv.writer(op1)
for i in range(len(f1mod)):
    vec = feature_vec(f1mod[i])
    writer.writerow(vec)

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
    vec = feature_vec(f2mod[i])
    writer.writerow(vec)


