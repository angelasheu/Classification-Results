import re

def process_docs(docs):
    for i in range(len(docs)):
        cats, text = docs[i].split('\n')[0], ' '.join(docs[i].split('\n')[1:])
        text = re.sub(r'\s+', ' ', text).rstrip()
        # Store as tuple of category and text with extra whitespace and newlines removed
        docs[i] = (cats, text)
    #print docs

def main():
    inputfile = 'categorized_text_edited.txt'
    docfilename = 'cte_docfile';
    fo = open(inputfile)
    file_content = fo.read();
    fo.close();
    docs = file_content.split('*DELIM*')
    process_docs(docs)
    '''
    categories = docs[0]
    print docs[1].split('\n')
    docs[1] = re.sub(r'\s+', ' ', docs[1])
    docs[1] = docs[1].rstrip()
    print docs[1]
    '''

    target = open(docfilename, 'w')
    clabel = open(docfilename + '.rlabel', 'w');
    for i in range(1, len(docs)):
        clabel.write(docs[i][0] + '\n');
        target.write(docs[i][1] + '\n');
    target.close()


if __name__ == "__main__":
    main()
