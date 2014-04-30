# SVM Classification
SVM classification with no augmentations, with clustering, and with dimensionality reduction. Also performed Naive Bayes analysis with [harthur/classifier](https://github.com/harthur/classifier).

### cluto: 
CLMethod=RB. Computed clusters used as meta-features in document feature vectors. 

### svm_light:
Utilized default kernel, binary classifier for each cluster. 
"nc" denotes classification done without clustering metafeatures. 
<code>test_documents_key</code> corresponds to the correct classification for the test documents. 

### doc2mat-1.0:
*tfidf.py*- transforms a given matfile (generated from running doc2mat script) into .dat file.

  <code>Input arguments: [name of .mat file] [name of .dat file (optional)]</code>

### Clustering results found in svm_light
*3c_, 4c_, 5c_*- clustering done with 3, 4, and 5 clusters respectively, using TF-IDF of trigrams. Training documents put into groups based on 
clustering performed with only the training documents (as opposed to with the testing docs). 

### cte files
Classification performed with larger data set, using <code>categorized_text_edited.txt</code>.
<code>doc2mat_cte.py</code>- converts <code>categorized_text_edited.txt</code> into docfile compatible with cluto and generates corresponding .rlabel file. 

### full_data_plots:
.ps files for <code>cte_docfile</code>
