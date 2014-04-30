# -*- coding: utf-8 -*-
import sys
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.util import ngrams
from scipy import stats # Use for dimensionality reduction

num_grams = 3 # n-gram parameter
ngram_set = set()

'''
Eliminates stopwords from each of the documents, also transforms each of documents into a
list of words.
'''
def eliminate_stopwords(docs):
    for i in range(len(docs)):
        words = docs[i].split(' ')
        words = [ w.strip(string.punctuation) for w in words ]
        filtered_words = [w for w in words if not w in stopwords.words('english')]
        docs[i] = filtered_words

'''
Uses Porter Stemming algorith to stem words. Also converts all words to lowercase.
'''
def stem_words(docs):
    pstem = PorterStemmer()
    for i in range(len(docs)):
        words = [ pstem.stem(w).lower() for w in docs[i] ]
        docs[i] = words

'''
Populates set of all nGrams, transforms each of documents into a list of ngram tuples.
'''
def getNGrams(docs):
    docs_copy = list(docs)
    n = 1
    for _ in range(num_grams): #n-gram parameter
        for i in range(len(docs)):
            joined_words = ' '.join(docs_copy[i])
            grams = ngrams(joined_words.split(), n)
            for gram in grams:
                ngram_set.add(tuple(gram))
            if _ == 0:
                docs[i] = grams
            else:
                if grams != []:
                    for gram in grams:
                        docs[i].append(gram)
        n += 1

'''
@return document_vectors a list documents vectorized by ngram count, also returns word_count list
'''
def vectorize(docs, all_ngrams):
    document_vectors = []
    word_count = [ 0 for x in range(len(all_ngrams)) ] # Word count for ALL ngrams
    for i in range(len(docs)):
        doc = docs[i]
        doc_vector = [0 for x in range(len(all_ngrams))]

        for gram in doc:
            gram = tuple(gram)
            if gram in all_ngrams:
                v_i = all_ngrams.index(gram)
                word_count[v_i] += 1
                doc_vector[v_i] += 1
        document_vectors.append(doc_vector)

    return document_vectors, word_count

def remove_features(all_ngrams, to_remove):
    all_ngrams_reduced = []
    to_remove = [x[0] for x in to_remove]
    for gram in all_ngrams:
        if gram not in to_remove:
            all_ngrams_reduced.append(gram)
    return all_ngrams_reduced

def process_vectors(doc_vectors):
    non_zero_entries = 0
    doc_vec_str = []
    for vec in doc_vectors:
        vec_str = ''
        for i in range(len(vec)):
            if vec[i] != 0:
                non_zero_entries += 1;
                vec_str += str(i+1) + ' ' + str(vec[i]) + ' '
        vec_str += '\n'
        doc_vec_str.append(vec_str)
    return doc_vec_str, non_zero_entries

# Returns an array of (ngram, stdev) to remove from features list
def get_stats_and_features_to_remove(word_count, all_ngrams):
    print 'Word count: ', len(word_count)
    z_scores = stats.zscore(word_count)

    std_1 = 0
    std_2 = 0
    std_3 = 0
    std_1_ls = []
    std_2_ls = []
    std_3_ls = []
    i = 0

    for z in z_scores:
        #print z
        if z >= 1 or z <= -1:
            std_1 += 1
            if not (z >= 2 or z <= -2):
                std_1_ls.append(all_ngrams[i])
            if z >= 2 or z <= -2:
                std_2 += 1
                if not (z >= 3 or z <= -3):
                    std_2_ls.append((all_ngrams[i], z))
                if z >= 3 or z <= -3:
                    std_3_ls.append((all_ngrams[i], z))
                    std_3 += 1
        i += 1
    print 'std_1: ', std_1
    print 'std_2: ', std_2
    print 'std_3: ', std_3

    print '\ngrams in std_2: '
    for gram in std_2_ls:
        print gram


    print '\ngrams in std_3: '
    for gram in std_3_ls:
        print gram

    to_remove = []
    to_remove.extend(std_2_ls)
    to_remove.extend(std_3_ls)

    return to_remove



def main(argv):
    inputfile = argv[0]
    matfilename = argv[1] if len(argv) > 1 else inputfile + 'matfile';
    fo = open(inputfile)
    file_content = fo.read();
    print 'Read file content'
    fo.close();
    docs = file_content.split('\n')[:-1]

    eliminate_stopwords(docs)
    print 'eliminated stop words'

    stem_words(docs)
    print 'stemmed words'


    getNGrams(docs)
    print 'processed ngrams'
    all_ngrams = list(ngram_set)


    document_vectors, word_count = vectorize(docs, all_ngrams)
    #doc_vec_str, non_zero_entries = process_vectors(document_vectors)

    print 'Before dimensionality reduction, num_features is ', len(all_ngrams)


    to_remove = get_stats_and_features_to_remove(word_count, all_ngrams)
    all_ngrams = remove_features(all_ngrams, to_remove)
    document_vectors, word_count = vectorize(docs, all_ngrams)

    print 'After dimensionality reduction, num_features is ', len(all_ngrams)
    doc_vec_str, non_zero_entries = process_vectors(document_vectors)

    # First line of matfile needs to contain (num_docs, num_columns, num_non_zero_entries)
    num_docs = len(docs)
    num_columns = len(all_ngrams)

    # Write results to matfile
    target = open(matfilename, 'w')
    target.write(str(num_docs) + ' ' + str(num_columns) + ' ' + str(non_zero_entries) + '\n')
    for vec_str in doc_vec_str:
        target.write(vec_str)
    target.close()

    print 'matfile written'

    #Write .clabel file
    target = open(matfilename + '.clabel', 'w')
    for i in range(len(all_ngrams)):
        target.write(str(all_ngrams[i]) + '\n')
    target.close()

    print '.clabel written'


if __name__ == "__main__":
    main(sys.argv[1:])
