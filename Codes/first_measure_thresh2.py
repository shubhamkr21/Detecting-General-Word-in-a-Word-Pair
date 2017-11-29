
import re

def takeSecond(elem):
    return elem[1]


def takeFirst(elem):
	return elem[0]


def run(first,second):
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
		            id_weight_tuple = (int(id_weight[0]), float(id_weight[1]))
		            listword1.append(id_weight_tuple)
		            i = i + 1

		    if word_noun_id[1] == id:
		        count2 = count2 + 1
		        size = len(id_edge)
		        i = 1
		        while i < size:
		            id_weight = id_edge[i].split('$_$_$')
		            id_weight_tuple = (int(id_weight[0]), float(id_weight[1]))
		            listword2.append(id_weight_tuple)
		            i = i + 1
		    if count2 == 2:
		        break
    
    listword1.sort(key=takeSecond,reverse=True)
    listword2.sort(key=takeSecond,reverse=True)

    #print listword1[:10]
    #print listword2[:10]
    #print len(listword1)
    #print len(listword2)

    #print listword1
    #print listword2

    size1 = min(len(listword1),200)
    size2 = min(len(listword2),200)
    sum_degree1 = 0
    sum_degree2 = 0
    index1 = 0
    index2 = 0

    listword1 = listword1[:size1]
    listword2 = listword2[:size2]

    listword1.sort(key=takeFirst)
    listword2.sort(key=takeFirst)

    #print listword1
    #print len(listword1)

    count = 0
    with open("Full_context_word_edges") as f:
		for line in f:
		    id_context = re.findall(r'\S+', line)
		    id = id_context[0]

		    #print (listword1[index1][0]," ", id) 

		    if int(listword1[index1][0]) == int(id):
		        index1 = index1 + 1
		        if index1 == size1:
		        	count = count + 1
		        	index1 = 0
		        sum_degree1 = sum_degree1 + len(id_context) - 1

		    if int(listword2[index2][0]) == int(id):
		        index2 = index2 + 1
		        if index2 == size2:
		        	count = count + 1
		        	index2 = 0
		        sum_degree2 = sum_degree2 + len(id_context) - 1

		    if count == 2:
		        break


    avg_degree1 = (sum_degree1) / (1.0*size1)
    avg_degree2 = (sum_degree2) / (1.0*size2)

    #print ("avgerage degree of first word contexts =", avg_degree1)
    #print ("avgerage degree of second word contexts =", avg_degree2)
    if avg_degree1 >= avg_degree2:
		print first,second
		print first
    else:
		print first,second
		print second 

if __name__ == "__main__":    
	line_count = 0    
	with open('output.txt') as f:
		for line in f:
			line_count = line_count + 1
			token = re.findall(r'\S+', line)
			run(token[0],token[1])



