Results for SVM Classification augmented with clustering. 
Used doc2mat to convert text files to .mat files that were then converted to .dat files for
classification using SVM light. Clusters computed using cluto. 

svmlight:
Utilized default kernel, binary classifier for each cluster. 
"nc" denotes classification done without clustering metafeatures. 
test_documents_key corresponds to the correct classification for the test documents. 

doc2mat-1.0:
tfidf.py- transforms a given matfile (generated from running doc2mat script) into .dat file.
Input arguments: [name of .mat file] [name of .dat file (optional]



