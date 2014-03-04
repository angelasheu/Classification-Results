#!/usr/bin/python

from __future__ import division
import sys
import numpy
from numpy import linalg as LA

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

def create_dat_file(vector_list, filename):
    target = open(filename, 'w')
    for v in vector_list:
        comb_list = zip(v[1], v[0])
        comb_list.sort()
        target.write('-1 ') # By default initialize all SVM feature vector labels to -1
        for i in range(len(comb_list)):
            target.write(str(comb_list[i][0]) + ':' + str(comb_list[i][1]) + ' ')
        target.write('\n')

    print '.dat file written'
    target.close()


def main(argv):
    inputfile = argv[0]
    filename = argv[1] if len(argv) > 1 else inputfile + '.dat'
    print 'Processing matrix file ', inputfile, ", writing .dat file to ", filename
    fo = open(inputfile)
    file_content = fo.read();
    fo.close();
    docs = file_content.split('\n')[:-1]
    wc_dict = count_doc_frequency(docs)
    vector_list = compute_tfidf(docs[1:], wc_dict)
    create_dat_file(vector_list, filename)

if __name__ == "__main__":
    main(sys.argv[1:])
