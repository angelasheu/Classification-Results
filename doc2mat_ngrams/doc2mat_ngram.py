import sys
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.util import ngrams

n = 3 # n-gram parameter
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
    for _ in range(3):
        for i in range(len(docs)):
            joined_words = ' '.join(docs_copy[i])
            grams = ngrams(joined_words.split(), n)
            for gram in grams:
                ngram_set.add(tuple(gram))
            docs[i] = grams
        n += 1
# Add n-gram to hashset

'''
@return document_vectors a list documents vectorized by ngram count
'''
def vectorize(docs, all_ngrams):
    document_vectors = []
    for i in range(len(docs)):
        doc = docs[i]
        doc_vector = [0 for x in range(len(all_ngrams))]
        for gram in doc:
            gram = tuple(gram)
            if gram in all_ngrams:
                v_i = all_ngrams.index(gram)
                doc_vector[v_i] += 1
        document_vectors.append(doc_vector)

    return document_vectors

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


def main(argv):
    inputfile = argv[0]
    matfilename = argv[1] if len(argv) > 1 else 'matfile';
    fo = open(inputfile)
    file_content = fo.read();
    fo.close();
    docs = file_content.split('\n')[:-1]

    eliminate_stopwords(docs)
    stem_words(docs)
    getNGrams(docs)
    all_ngrams = list(ngram_set)
    document_vectors = vectorize(docs, all_ngrams)
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

    #Write .clabel file
    target = open(matfilename + '.clabel', 'w')
    for i in range(len(all_ngrams)):
        target.write(str(all_ngrams[i]) + '\n')
    target.close()

if __name__ == "__main__":
    main(sys.argv[1:])
