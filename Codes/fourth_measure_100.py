import re
import math
from math import log

def takeSecond(elem):
    return elem[1]

def takeFirst(elem):
    return elem[0]

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def run(first,second):
    #first = raw_input("Enter the first word: ")
    #second = raw_input("Enter the second word: ")
    #print(first)
    #print(second)
    word_noun_id = ['-1', '-1']
    word_adjective_id = [-1, -1]
    word_verb_id = [-1, -1]
    count = 0
    with open("Full_word_nodes") as f:
        for line in f:
            word_id = re.findall(r'\S+', line)
            word = word_id[0].split('/')
            if first == word[0]:
                if word[1] == 'NN':
                        word_noun_id[0] = word_id[1]
                        count = count + 1
            if second == word[0]:
                if word[1] == 'NN':
                        word_noun_id[1] = word_id[1]
                        count =  count + 1
            if count == 2:
                break;
    #print word_noun_id
    if word_noun_id[0] == '-1' or word_noun_id[1] == '-1':
    	return 

    count2 = 0
    listword1 = []
    listword2 = []
    with open("Full_word_context_edges") as f:
        for line in f:
            id_edge = re.findall(r'\S+', line)
            id = id_edge[0]
            if word_noun_id[0] == id:
                count2 = count2 + 1
                size = len(id_edge)
                i = 1
                while i < size:
                    id_weight = id_edge[i].split('$_$_$')
                    id_weight_tuple = (int(id_weight[0]), id_weight[1])
                    listword1.append(id_weight_tuple)
                    i = i + 1

            if word_noun_id[1] == id:
                count2 = count2 + 1
                size = len(id_edge)
                i = 1
                while i < size:
                    id_weight = id_edge[i].split('$_$_$')
                    id_weight_tuple = (int(id_weight[0]), id_weight[1])
                    listword2.append(id_weight_tuple)
                    i = i + 1
            if count2 == 2:
                break
    
    listword1.sort(key=takeSecond,reverse=True)
    listword2.sort(key=takeSecond,reverse=True)

    NofN1 = []
    NofN2 = []
    index1 = 0
    index2 = 0
    size1 = min(100,len(listword1))
    size2 = min(100,len(listword2))

    listword1 = listword1[:size1]
    listword2 = listword2[:size2]

    listword1.sort(key=takeFirst)
    listword2.sort(key=takeFirst)

    context_degree1 = []
    context_degree2 = []

    with open("Full_context_word_edges") as f:
        for line in f:
            id_context = re.findall(r'\S+', line)
            id = id_context[0]

            if int(listword1[index1][0]) == int(id):
                index1 = index1 + 1
                if index1 == size1:
                    index1 = 0
                size = len(id_context)
                i = 1
                while i < size:
                    id_context_weight = id_context[i].split('$_$_$')
                    NofN1.append(int(id_context_weight[0]))
                    i = i + 1
                elem = len(id_context)-1
                context_degree1.append(elem)

            if int(listword2[index2][0]) == int(id):
                index2 = index2 + 1
                if index2 == size2:
                    index2 = 0
                i = 1
                size = len(id_context)
                while i < size:
                    id_context_weight = id_context[i].split('$_$_$')
                    NofN2.append(int(id_context_weight[0]))
                    i = i + 1
                elem = len(id_context)-1
                context_degree2.append(elem)

            if index1 == size1 and index2 == size2:
                break

    NofN1.sort()
    NofN2.sort()
    

    NofN1_set = list(set(NofN1))
    NofN2_set = list(set(NofN2))

    index1 = 0
    for i in NofN1_set:
        count = 0
        while i == NofN1[index1]:
            count = count + 1
            index1 = index1 + 1
        context_degree1.append(count)

    index2 = 0
    for i in NofN2_set:
        count = 0
        while i == NofN2[index2]:
            count = count + 1
            index2 = index2 + 1
        context_degree2.append(count)

    index1 = 0
    index2 = 0
    
    context_degree1.sort()
    context_degree2.sort()

    total_elem1 = len(context_degree1)
    total_elem2 = len(context_degree2)

    context_degree1_set = []
    context_degree2_set = []

    context_degree1_set = list(set(context_degree1))
    context_degree2_set = list(set(context_degree2))

    index1 = 0
    index2 = 0

    entropy1 = 0
    entropy2 = 0

    for i in context_degree1_set:
        count = 0
        while index1 < len(context_degree1) and i == context_degree1[index1]:
            count = count + 1
            index1 = index1 + 1
        if(index1 == len(context_degree1)):
            break
        pi1 = float(count*1.0/total_elem1)
        if isclose(pi1,0.0) is False:
            entropy1 = entropy1 + pi1 * math.log(pi1)

    for i in context_degree2_set:
        count = 0
        while index2 < len(context_degree2) and i == context_degree2[index2]:
            count = count + 1
            index2 = index2 + 1
        if(index2 == len(context_degree2)):
            break
        pi2 = float(count*1.0/total_elem2)
        if isclose(pi2,0.0) is False:
            entropy2 = entropy2 + pi2 * math.log(pi2)
        
    if entropy1 >= entropy2:
    	print first,second
    	print first
    else:
    	print first,second
    	print second 
    #print ("entropy1=", entropy1)
    #print ("entropy2=", entropy2)


if __name__ == "__main__": 
    line_count = 0
    with open('output.txt') as f:
        for line in f:
	    line_count = line_count + 1
	    token = re.findall(r'\S+',line)
            run(token[0],token[1])
