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

    target = open(docfilename, 'w')
    clabel = open(docfilename + '.rlabel', 'w');
    for i in range(1, len(docs)):
        clabel.write(docs[i][0] + '\n');
        target.write(docs[i][1] + '\n');
    target.close()

    print 'categories in training set: ', categories_seen


if __name__ == "__main__":
    main()
