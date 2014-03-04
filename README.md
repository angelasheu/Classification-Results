# SVM Classification augmented with clustering. 
Used doc2mat to convert text files to .mat files that were then converted to .dat files for
classification using SVM light. Clusters computed using cluto. 

## cluto: 
CLMethod=RB. Computed clusters used as meta-features in document feature vectors. 

## svm_light:
Utilized default kernel, binary classifier for each cluster. 
"nc" denotes classification done without clustering metafeatures. 
test_documents_key corresponds to the correct classification for the test documents. 

## doc2mat-1.0:
*tfidf.py*- transforms a given matfile (generated from running doc2mat script) into .dat file.

Input arguments: [name of .mat file] [name of .dat file (optional]

## Clustering results found in svm_light
*3c_, 4c_, 5c_*- clustering done with 3, 4, and 5 clusters respectively, using TF-IDF of trigrams. Training documents put into groups based on 
clustering performed with only the training documents (as opposed to with the testing docs). 
