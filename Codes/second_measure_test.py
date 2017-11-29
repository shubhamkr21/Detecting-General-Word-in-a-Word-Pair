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
    if word_noun_id[0] == '-1' or word_noun_id[1] == '-1':
        return ('-1','-1')
    print first,second
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
    
    listword1.sort(key=takeSecond)
    listword2.sort(key=takeSecond)

    
    NofN1 = []
    NofN2 = []
    index1 = 0
    index2 = 0
    size1 = len(listword1)
    size2 = len(listword2)

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

            if index1 == size1 and index2 == size2:
                break

    NofN1.sort()
    NofN2.sort()

    size = len(NofN1)
    count1 = 1
    prev = NofN1[0]
    i = 1
    while i < size:
        if NofN1[i] != prev:
            count1 = count1 + 1
        i = i + 1

    size = len(NofN2)
    count2 = 1
    prev = NofN2[0]
    i = 1
    while i < size:
        if NofN2[i] != prev:
            count2 = count2 + 1
        i = i + 1    
    if count1 >= count2:
        return (first,first)
    else:
        return (first,second)
    


if __name__ == "__main__": 
    res = []
    test_count = 0
    line_count = 0
    with open('output.txt') as f:
        for line in f:
            line_count = line_count + 1
            token = re.findall(r'\S+', line)
            _tuple = run(token[0],token[1])
            if _tuple != ('-1','-1'):
                test_count = test_count+1
                print _tuple[1]
                res.append(_tuple)
