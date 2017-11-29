import re

def takeSecond(elem):
    return elem[0]

def run(first,second):
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

    count2 = 0
    listword1 = []
    listword2 = []
    avgweight = 0

    array = []
    with open("Full_context_nodes") as f:
        for line in f:
            word = re.findall(r'\S+', line)
            word_tag = word[0].split('/')
            #print word_tag
            if word_tag[2].startswith("JJ"):
                #print "appended" 
                array.append(int(word[1]))

    with open("Full_word_context_edges") as f:
        
        for line in f:
            id_edge = re.findall(r'\S+', line)
            id = id_edge[0]

            if word_noun_id[0] == id:
                count2 = count2 + 1
                size = len(id_edge)
                i = 1
                index = 0
                max_index = len(array)
                while i < size:
                    id_weight = id_edge[i].split('$_$_$')
                    #print id_weight[0], "bahh", array[index]
                    while int(index) < int(max_index) and int(id_weight[0]) > int(array[index]):
                        #print "id=", id_weight[0], "array[index]=", array[index]
                        index = index + 1
                    if max_index == index:
                        break
                    if int(id_weight[0]) == int(array[index]):
                        avgweight = avgweight + float(id_weight[1])
                        id_weight_tuple = (int(id_weight[0]), id_weight[1])
                        #print "appended list 1"
                        listword1.append(id_weight_tuple)
                    i = i + 1

            if word_noun_id[1] == id:
                count2 = count2 + 1
                size = len(id_edge)
                i = 1
                index = 0
                max_index = len(array)
                while i < size:
                    id_weight = id_edge[i].split('$_$_$')
                    while int(index) < int(max_index) and int(id_weight[0]) > int(array[index]):
                        #print "id=", id_edge[i], "array[index]=", array[index]
                        index = index + 1
                    if int(max_index) == int(index):
                        break
                    if int(id_weight[0]) == int(array[index]):
                        #print "appended list 2"
                        avgweight = avgweight + float(id_weight[1])
                        id_weight_tuple = (int(id_weight[0]), id_weight[1])
                        listword2.append(id_weight_tuple)
                    i = i + 1
            if count2 == 2:
                break

    #print listword1
    #print listword2
    suml = len(listword1) + len(listword2)
    avgweight = 10000
    if suml != 0:
    	avgweight = (avgweight)/(suml)

    list1 = []

    for i in listword1:
        #print i[1]
        #print (";ist1 i[1] = ",i[1], " maxweight=", maxweight)
        if float(i[1]) > avgweight:
            #print("appended")
            list1.append(i)

    list2 = []
    for i in listword2:
        #print ("list 2 i[1] = ",i[1], " maxweight=", maxweight)
        if float(i[1]) > avgweight:
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
    if second_minus_first == 0:
        ratio = 100000.0
    else :
        ratio = (float(first_minus_second)/second_minus_first)
    #print ("ratio calculated is " , ratio)

    '''
        Change the threshold value and get the accuracy 
        mandal tere liye test krne k liye
        yeh niche wali thresholding hata bhi sakta hai
        but agar comaparable result aaya ..wo wale case mai kaam aayegi yeh bas
        tu average measyre bhi change krke dekh sakta hai
        completed 
    '''
    high_threshold = 2.0
    low_threshold = 0.5
    if ratio > high_threshold:
        print first,second
        print first 
    elif ratio < low_threshold:
        print first,second
        print second 
    else:
        pass


if __name__ == "__main__":
    line_count = 0
    with open('output.txt') as f:
        for line in f:
            line_count = line_count + 1
            token = re.findall(r'\S+',line)
            run(token[0],token[1])
