#!/usr/bin/python

from __future__ import division
import sys
import numpy
import re
import os
from numpy import linalg as LA

# Change this to get correct categories
clustering_num = 7

def count_doc_frequency(docs):
    # Initialize dictionary
    words_total = docs[0].split(' ')[1]
    wc_dict = {}
    for i in range(1, int(words_total)+1):
        wc_dict[i] = 0
    for doc in docs[1:]:
        curr = filter(None, doc.split(' '))
        for i in range(0, len(curr), 2):
            wc_dict[int(curr[i])] += int(curr[i+1])

    return wc_dict

def compute_tfidf(docs, wc_dict):
    vector_list = []
    for doc in docs:
        curr = filter(None, doc.split(' '))
        vector = []
        id_list = []
        for i in range(0, len(curr), 2):
            word_id, tf = int(curr[i]), int(curr[i+1])
            if tf > 0:
                vector.append( tf * numpy.log2( len(docs) / wc_dict[word_id] ) )
                id_list.append(word_id)
        norm = LA.norm(vector)
        vector = vector / norm
        vector_list.append((vector, id_list))
    return vector_list

def get_cats():

    cats = {}

    fo = open('cte_matfile.clustering.' + str(clustering_num))
    cluster_nums = fo.read().split('\n')[:-1]
    print 'CLUSTER_NUMS: ', cluster_nums
    fo.close()

    fo = open('tfidf_labels')
    labels = fo.read().split('\n')[:-1]
    fo.close()

    for i in range(0, len(cluster_nums)):
        tr_label = [re.sub(' ', '', s) for s in (re.sub('[\[\]]', '', labels[i])).split(',')]
        cluster = cluster_nums[i]
        for i in range(len(tr_label)):
            if tr_label[i] == "'*'":
                if cluster not in cats:
                    cats[cluster] = []
                if (i+1) not in cats[cluster]:
                    cats[cluster].append(i+1)

    ret_list = []
    print 'DICTIONARY: ', cats
    for key in cats:
        c_list = cats[key]
        c_list.sort()
        ret_list.append(c_list)

    return ret_list

# Creat .dat file using clusters as categories
def create_dat_file_10(vector_list):
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

    # Create a _train.dat file for each category
    for c in cats:
        directory = 'cat' + str(c)
        #filename = 'cat' + str(c) + '_train.dat'

        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = directory + '/cat' + str(c) + '_train.dat'


        target = open(filename, 'w')
        count = 0
        for v in vector_list:
            labels = vec_labels_list[count]

            # Combine feature # and count together
            comb_list = zip(v[1], v[0])
            comb_list.sort()

            if c in labels:
                target.write('1 ')
            else:
                target.write('-1 ')

            for i in range(len(comb_list)):
                target.write(str(comb_list[i][0]) + ':' + str(comb_list[i][1]) + ' ')
            target.write('\n')
            count += 1

        print filename, ' written'
        target.close()


def create_dat_file(vector_list):

    #cats = [1, 2, 3, 5, 6, 9, 10, 13, 14]
    #cats = [ [4, 6, 10], [1, 3, 6, 9, 13], [2, 9], [5, 9, 14], [6, 9] ]
    cats = get_cats()

    print 'CATS: ', cats

    fo = open('tfidf_labels')
    file_content = fo.read()
    fo.close()

    lines = file_content.split('\n')[:-1]
    vec_labels_list = []
    for i in range(0, len(lines)):
        labels = []
        c = [re.sub(' ', '', s) for s in (re.sub('[\[\]]', '', lines[i])).split(',')]

        for j in cats:
            for l in j:
                if c[l-1] == "'*'":
                    labels.append(l)
        vec_labels_list.append(labels)

    # Create a _train.dat file for each category in its own folder

    for c in cats:
        directory = 'cat' + str(c)
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = directory + '/cat' + str(c) + '_train.dat'
        target = open(filename, 'w')
        count = 0
        for v in vector_list:
            labels = vec_labels_list[count]

            # Combine feature # and count together
            comb_list = zip(v[1], v[0])
            comb_list.sort()

            set_true = False
            for c_s in c:
                if c_s in labels: set_true = True


            if set_true:
                target.write('1 ')
            else:
                target.write('-1 ')

            for i in range(len(comb_list)):
                target.write(str(comb_list[i][0]) + ':' + str(comb_list[i][1]) + ' ')
            target.write('\n')
            count += 1

        print filename, ' written'
        target.close()


def main(argv):
    inputfile = argv[0]
    fo = open(inputfile)
    file_content = fo.read();
    fo.close();
    docs = file_content.split('\n')[:-1]
    wc_dict = count_doc_frequency(docs)
    vector_list = compute_tfidf(docs[1:], wc_dict)
    create_dat_file_10(vector_list)
    #create_dat_file(vector_list)

if __name__ == "__main__":
    main(sys.argv[1:])
