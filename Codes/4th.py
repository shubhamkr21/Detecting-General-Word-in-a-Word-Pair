import re
import math
from math import log

def takeSecond(elem):
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
    if word_noun_id[0] == '-1' or word_noun_id[1] == '-1':
    	return

    count2 = 0
    listword1 = []
    listword2 = []
    maxweight = 0

    nounarray = []
    adjarray = []
    verbarray = []

    print first,second 

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
                    if maxweight < float(id_weight[1]):
                        maxweight = float(id_weight[1])
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
                    if maxweight < float(id_weight[1]):
                        maxweight = float(id_weight[1])
                    listword2.append(id_weight_tuple)
                    i = i + 1
            if count2 == 2:
                break
    

    listword1.sort(key=takeSecond)
    listword2.sort(key=takeSecond)

    indexlist1 = 0
    indexlist2 = 0

    adj_list1 = []
    noun_list1 = []
    verb_list1 = []
    adj_list2 = []
    noun_list2 = []
    verb_list2 = []

    count = 0
    with open("Full_context_nodes") as f:
        for line in f:
            word = re.findall(r'\S+', line)
            word_tag = word[0].split('/')
            if indexlist1 < len(listword1) and int(word[1]) == int(listword1[indexlist1][0]):
                if word_tag[2].startswith("JJ"):
                    adj_list1.append(listword1[indexlist1])

                if word_tag[2].startswith("NN"):
                    noun_list1.append(listword1[indexlist1])

                if word_tag[2].startswith("VB"):
                    verb_list1.append(listword1[indexlist1])

                indexlist1 = indexlist1 + 1
                if indexlist1 == len(listword1):
                    count = count + 1


            if indexlist2 < len(listword2) and int(word[1]) == int(listword2[indexlist2][0]):
                if word_tag[2].startswith("JJ"):
                    adj_list2.append(listword2[indexlist2])

                if word_tag[2].startswith("NN"):
                    noun_list2.append(listword2[indexlist2])


                if word_tag[2].startswith("VB"):
                    verb_list2.append(listword2[indexlist2])
                    

                indexlist2 = indexlist2 + 1
                if indexlist2 == len(listword2):
                    count = count + 1
            if count == 2:
                break

    index1 = 0
    index2 = 0
    size1 = len(noun_list1)
    size2 = len(noun_list2)
    context_degree_noun1 = []
    context_degree_noun2 = []

    with open("Full_context_word_edges") as f:
        for line in f:
            id_context = re.findall(r'\S+', line)
            id = id_context[0]

            if index1 < size1 and int(noun_list1[index1][0]) == int(id):
                index1 = index1 + 1
                if index1 == size1:
                    index1 = 0
                elem = len(id_context)-1
                context_degree_noun1.append(elem)

            if index2 < size2 and int(noun_list2[index2][0]) == int(id):
                index2 = index2 + 1
                if index2 == size2:
                    index2 = 0
                elem = len(id_context)-1
                context_degree_noun2.append(elem)

            if index1 == size1 and index2 == size2:
                break

    context_degree_noun1.sort()
    context_degree_noun2.sort()

    total_elem1 = len(context_degree_noun1)
    total_elem2 = len(context_degree_noun2)

    context_degree_noun1_set = []
    context_degree_noun2_set = []

    context_degree_noun1_set = list(set(context_degree_noun1))
    context_degree_noun2_set = list(set(context_degree_noun2))

    index1 = 0
    index2 = 0

    entropy1 = 0
    entropy2 = 0

    for i in context_degree_noun1_set:
        count = 0
        while index1 < len(context_degree_noun1) and i == context_degree_noun1[index1]:
            count = count + 1
            index1 = index1 + 1
        if(index1 == len(context_degree_noun1)):
            break
        pi1 = float(count*1.0/total_elem1)
        if isclose(pi1,0.0) is False:
            entropy1 = entropy1 + pi1 * math.log(pi1)

    for i in context_degree_noun2_set:
        count = 0
        while index2 < len(context_degree_noun2) and i == context_degree_noun2[index2]:
            count = count + 1
            index2 = index2 + 1
        if(index2 == len(context_degree_noun2)):
            break
        pi2 = float(count*1.0/total_elem2)
        if isclose(pi2,0.0) is False:
            entropy2 = entropy2 + pi2 * math.log(pi2)
        
    print "++++++considering noun tags++++++++\n"
    print ("entropy1=", entropy1)
    print ("entropy2=", entropy2)

    if entropy1 >= entropy2:
    	print first
    else:
    	print second 

    index1 = 0
    index2 = 0
    size1 = len(verb_list1)
    size2 = len(verb_list2)
    context_degree_verb1 = []
    context_degree_verb2 = []

    with open("Full_context_word_edges") as f:
        for line in f:
            id_context = re.findall(r'\S+', line)
            id = id_context[0]

            if size1 < index1 and int(verb_list1[index1][0]) == int(id):
                index1 = index1 + 1
                if index1 == size1:
                    index1 = 0
                elem = len(id_context)-1
                context_degree_verb1.append(elem)

            if size2 < index2 and int(verb_list2[index2][0]) == int(id):
                index2 = index2 + 1
                if index2 == size2:
                    index2 = 0
                elem = len(id_context)-1
                context_degree_verb2.append(elem)

            if index1 == size1 and index2 == size2:
                break

    context_degree_verb1.sort()
    context_degree_verb2.sort()

    total_elem1 = len(context_degree_verb1)
    total_elem2 = len(context_degree_verb2)

    context_degree_verb1_set = []
    context_degree_verb2_set = []

    context_degree_verb1_set = list(set(context_degree_verb1))
    context_degree_verb2_set = list(set(context_degree_verb2))

    index1 = 0
    index2 = 0

    entropy1 = 0
    entropy2 = 0

    for i in context_degree_verb1_set:
        count = 0
        while index1 < len(context_degree_verb1) and i == context_degree_verb1[index1]:
            count = count + 1
            index1 = index1 + 1
        if(index1 == len(context_degree_verb1)):
            break
        pi1 = float(count*1.0/total_elem1)
        if isclose(pi1,0.0) is False:
            entropy1 = entropy1 + pi1 * math.log(pi1)

    for i in context_degree_verb2_set:
        count = 0
        while index2 < len(context_degree_verb2) and i == context_degree_verb2[index2]:
            count = count + 1
            index2 = index2 + 1
        if(index2 == len(context_degree_verb2)):
            break
        pi2 = float(count*1.0/total_elem2)
        if isclose(pi2,0.0) is False:
            entropy2 = entropy2 + pi2 * math.log(pi2)
        
    print "++++++considering verb tags++++++++\n"
    print ("entropy1=", entropy1)
    print ("entropy2=", entropy2)

    if entropy1 >= entropy2:
    	print first
    else:
    	print second 

    index1 = 0
    index2 = 0
    size1 = len(adj_list1)
    size2 = len(adj_list2)
    context_degree_adj1 = []
    context_degree_adj2 = []

    with open("Full_context_word_edges") as f:
        for line in f:
            id_context = re.findall(r'\S+', line)
            id = id_context[0]
            if size1!= index1 :
	            if int(adj_list1[index1][0]) == int(id):
	                index1 = index1 + 1
	                
	                elem = len(id_context)-1
	                context_degree_adj1.append(elem)
			if size2!= index2 :    
			    if int(adj_list2[index2][0]) == int(id):
					index2 = index2 + 1
	            	elem = len(id_context)-1
	            	context_degree_adj2.append(elem)

            if index1 == size1 and index2 == size2:
                break

    context_degree_adj1.sort()
    context_degree_adj2.sort()

    total_elem1 = len(context_degree_adj1)
    total_elem2 = len(context_degree_adj2)

    context_degree_adj1_set = []
    context_degree_adj2_set = []

    context_degree_adj1_set = list(set(context_degree_adj1))
    context_degree_adj2_set = list(set(context_degree_adj2))

    index1 = 0
    index2 = 0

    entropy1 = 0
    entropy2 = 0

    for i in context_degree_adj1_set:
        count = 0
        while index1 < len(context_degree_adj1) and i == context_degree_adj1[index1]:
            count = count + 1
            index1 = index1 + 1
        if(index1 == len(context_degree_adj1)):
            break
        pi1 = float(count*1.0/total_elem1)
        if isclose(pi1,0.0) is False:
            entropy1 = entropy1 + pi1 * math.log(pi1)

    for i in context_degree_adj2_set:
        count = 0
        while index2 < len(context_degree_adj2) and i == context_degree_adj2[index2]:
            count = count + 1
            index2 = index2 + 1
        if(index2 == len(context_degree_adj2)):
            break
        pi2 = float(count*1.0/total_elem2)
        if isclose(pi2,0.0) is False:
            entropy2 = entropy2 + pi2 * math.log(pi2)
        
    print "++++++considering adj tags++++++++\n"
    print ("entropy1=", entropy1)
    print ("entropy2=", entropy2)

    if entropy1 >= entropy2:
    	print first
    else:
    	print second 
    
if __name__ == "__main__":
	line_count = 0    
	with open('output.txt') as f:
		for line in f:
			line_count = line_count + 1
			#if line_count <= 660:
			#	continue
			token = re.findall(r'\S+', line)
			run(token[0],token[1])
