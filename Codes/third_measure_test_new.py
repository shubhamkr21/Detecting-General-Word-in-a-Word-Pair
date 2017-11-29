import re

def takeSecond(elem):
    return elem[0]

def run(first,second):   
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


    list1 = []

    for i in listword1:
        #print i[1]
        #print (";ist1 i[1] = ",i[1], " maxweight=", maxweight)
        if float(i[1]) > (float(maxweight)/2.0):
            #print("appended")
            list1.append(i)

    list2 = []
    for i in listword2:
        #print ("list 2 i[1] = ",i[1], " maxweight=", maxweight)
        if float(i[1]) > (float(maxweight)/2.0):
            list2.append(i)

    #print ("size of list1=", len(list1), " size of listword1=", len(listword1))
    #print ("size of list2=", len(list2), " size of listword2=", len(listword2))


    list1.sort(key=takeSecond)
    list2.sort(key=takeSecond)

    #print list1
    #print list2

    size1 = len(list1)
    size2 = len(list2)
    i = 0
    j = 0
    first_minus_second = 0
    second_minus_first = 0
    while i < size1 and j < size2:
        if list1[i][0] == list2[j][0]:
            i = i + 1
            j = j + 1
        elif list1[i][0] < list2[j][0]:
            i = i + 1
            first_minus_second = first_minus_second + 1
        else:
            j = j + 1
            second_minus_first = second_minus_first + 1
    if i != size1:
        first_minus_second = first_minus_second + size1 - i
    if j != size2:
        second_minus_first = second_minus_first + size2 - j

    #print ("first - second count =" , first_minus_second)
    #print ("second - first count =" , second_minus_first)
    ratio = 11.0
    if second_minus_first != 0:
        ratio = (float(first_minus_second)/second_minus_first)
    #print ("ratio calculated is " , ratio)
    #high_threshold = 10.0
    #low_threshold = 0.1
    if first_minus_second >= second_minus_first:
        print first,second
        print first 
    else:
        print first,second 
        print second 
 

        


if __name__ == "__main__": 
    res = []
    test_count = 0
    line_count = 0
    with open('output.txt') as f:
        for line in f:
            line_count = line_count + 1
            token = re.findall(r'\S+', line)
            run(token[0],token[1])

