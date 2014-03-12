import sys

def main(argv):
    inputfile = 'cte_matfile'
    fo = open(inputfile)
    file_content = fo.read()
    fo.close()


    clustering_num = argv[0]
    clustering_file = 'cte_matfile.clustering.' + clustering_num
    print 'Adding meta-features based on ', clustering_file

    outputfile = 'cte_matfile_' + clustering_num

    fo = open(clustering_file)
    clustering_content = fo.read()
    fo.close()
    clustering_content = clustering_content.split('\n');

    lines = file_content.split('\n')
    base_featurenum = int(lines[0].split(' ')[1])
    doc_vecs = lines[1:]

    target = open(outputfile, 'w')

    # Change header info
    header_info = [int(x) for x in lines[0].split(' ')]
    header_info[1] += int(clustering_num)
    header_info[2] += header_info[0] # Each vector gets a non-zero feature entry added
    target.write(str(header_info[0]) + ' ' + str(header_info[1]) + ' ' + str(header_info[2]) + '\n')

    for i in range(len(doc_vecs)-1):
        #target.write(doc_vecs[i][:-1] + str(base_featurenum + int(clustering_content[i])) + ' 1 \n')

        metafeature_num = base_featurenum + int(clustering_content[i]) + 1 # Add 1 because cluto starts groups at 0
        to_write = doc_vecs[i][:-1] + ' ' + str(metafeature_num) + ' 1 \n'
        target.write(to_write)

    target.close()



if __name__ == "__main__":
    # Pass in 1 argument: Number of clusters used in cluto
    main(sys.argv[1:])
