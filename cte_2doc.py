import re
import ast

categories_seen = set()

def process_docs(docs):
    fo = open('tfidf_labels', 'w')
    for i in range(1, len(docs)):
        cats, text = docs[i].split('\n')[0], ' '.join(docs[i].split('\n')[1:])
        text = re.sub(r'\s+', ' ', text).rstrip()

        # Want to keep track of what categories we've seen
        c = (re.sub('[\[\]]', '', cats)).split(',')
        fo.write(str(c) + '\n')
        for j in range(len(c)):
            if c[j] == '*':
                categories_seen.add(j+1)

        # Store as tuple of category and text with extra whitespace and newlines removed
        docs[i] = (cats, text)
    fo.close()
    #print docs

def main():
    inputfile = 'categorized_text_edited.txt'
    docfilename = 'cte_docfile';
    fo = open(inputfile)
    file_content = fo.read();
    fo.close();
    docs = file_content.split('*DELIM*')

    process_docs(docs)

    testfile = 'testing_docs'
    fo = open(testfile)
    test_content = fo.read()
    fo.close()
    test_docs = test_content.split('\n')

    test_labels_file = 'testing_labels'
    fo = open(test_labels_file)
    file_content = fo.read()
    fo.close()
    test_labels = file_content.split('\n')

    target = open(docfilename, 'w')
    clabel = open('cte_matfile.rlabel', 'w');
    for i in range(1, len(docs)):
        clabel.write(docs[i][0] + '\n');
        target.write(docs[i][1] + '\n');
    for i in range(0, len(test_docs)):
        clabel.write(test_labels[i] + '\n')
        target.write(test_docs[i] + '\n')
    target.close()
    clabel.close()

    print 'categories in training set: ', categories_seen


if __name__ == "__main__":
    main()
