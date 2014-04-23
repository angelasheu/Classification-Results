import sys
import string
import doc2mat_ngram as ngram
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.util import ngrams
from scipy import stats
from ast import literal_eval

'''
Takes in docfile for test set and labels from training set. Outputs matfile for test docfile.
'''

# Turn testdoc array into array of ngrams. Does NOT populate a list of all_ngrams (did that for training docfile)
def get_NGrams(docs):
    docs_copy = list(docs)
    n = 1
    for _ in range(ngram.num_grams): #n-gram parameter
        for i in range(len(docs)):
            joined_words = ' '.join(docs_copy[i])
            grams = ngrams(joined_words.split(), n)
            if _ == 0:
                docs[i] = grams
            else:
                if grams != []:
                    for gram in grams:
                        docs[i].append(gram)
        n += 1

# Count occurrences for ngrams
def vectorize(docs, ngram_set):
    document_vectors = []
    for i in range(len(docs)):
        doc = docs[i]
        doc_vector = [0 for x in range(len(ngram_set))]

        for gram in doc:
            if gram in ngram_set:
                v_i = ngram_set.index(gram)
                doc_vector[v_i] += 1
        document_vectors.append(doc_vector)

    return document_vectors

def main(argv):
    inputfile = argv[0]
    ngramfile = argv[1]
    matfilename = argv[2] if len(argv) > 1 else inputfile + 'matfile';
    fo = open(inputfile)
    file_content = fo.read();

    fo.close();
    docs = file_content.split('\n')[:-1]

    ngram.eliminate_stopwords(docs)
    print 'eliminated stop words'

    ngram.stem_words(docs)
    print 'stemmed words'

    get_NGrams(docs)

    # Take in labels and build ngram_set from it
    fo = open(ngramfile)
    file_content = fo.read();
    fo.close();
    ngram_set = [literal_eval(s) for s in file_content.split('\n')[:-1]]

    document_vectors = vectorize(docs, ngram_set)
    doc_vec_str, non_zero_entries = ngram.process_vectors(document_vectors)

    # First line of matfile needs to contain (num_docs, num_columns, num_non_zero_entries); used for cluto/clustering
    num_docs = len(docs)
    num_columns = len(ngram_set)

    # Write results to matfile
    target = open(matfilename, 'w')
    target.write(str(num_docs) + ' ' + str(num_columns) + ' ' + str(non_zero_entries) + '\n')
    for vec_str in doc_vec_str:
        target.write(vec_str)
    target.close()


if __name__ == "__main__":
    # arg1 = test docfile, arg2 = training file labels, arg3 = matfilename
    main(sys.argv[1:])
