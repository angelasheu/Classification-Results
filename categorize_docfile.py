import re
import os

def write_pos_and_neg(docs):

    cats = [1, 2, 3, 5, 6, 9, 10, 13, 14]

    fo = open('tfidf_labels')
    file_content = fo.read()
    fo.close()

    lines = file_content.split('\n')[:-1]
    vec_labels_list = []

    for i in range(0, len(lines)):
        labels = []
        c = [re.sub(' ', '', s) for s in (re.sub('[\[\]]', '', lines[i])).split(',')]
        for j in cats:
            if c[j-1] == "'*'":
                labels.append(j)
        vec_labels_list.append(labels)


    # Create file
    directory = 'bayesian_data'
    if not os.path.exists(directory):
        os.makedirs(directory)


    for c in cats:
        filename_pos = directory + '/cat' + str(c) + '_pos'
        filename_neg = directory + '/cat' + str(c) + '_neg'


        target_p = open(filename_pos, 'w')
        target_n = open(filename_neg, 'w')
        count = 0

        for doc in docs:

            labels = vec_labels_list[count]

            if c in labels:
                target_p.write(docs[count] + '\n')
            else:
                target_n.write(docs[count] + '\n')

            count += 1

        print 'files for cat ', c , ' written'
        target_p.close()
        target_n.close()



def main():
    inputfile = 'cte_docfile_tronly'

    fo = open(inputfile)
    file_content = fo.read();
    fo.close()
    docs = file_content.split('\n')[:-1]
    write_pos_and_neg(docs)

if __name__ == "__main__":
    main()
