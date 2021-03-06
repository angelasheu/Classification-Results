#!/usr/bin/python
from subprocess import call
import sys

postfix = ''

def train(categories):
    for c in categories:
        call(["./svm_learn", c + "/" + c + postfix + "_train.dat", c + "/model" + postfix])

def classify(categories):
    for c in categories:
        print c, "/predictions", postfix
        call(["./svm_classify", c + "/test" + postfix + ".dat", c + "/model" + postfix, c + "/predictions" + postfix])

def train_nc(categories):
    for c in categories:
        call(["./svm_learn", c + "/train_nc.dat", c + "/model_nc"])

def classify_nc(categories):
    for c in categories:
        call(["./svm_classify", c + "/test_nc.dat", c + "/model_nc", c + "/predictions_nc"])


def main(argv):
    #categories = ['dropout', 'parent', 'PBIS', 'RTI', 'support', 'teaming', 'health']
    #categories = ['dropout_2', 'parent_2', 'PBIS_2', 'RTI_2', 'support_2', 'teaming_2', 'health_2']
    #categories = ['dropout_3', 'parent_3', 'PBIS_3', 'RTI_3', 'support_3', 'teaming_3', 'health_3']
    #categories = ['group1', 'group2', 'group3']
    #categories = ['3c_1', '3c_2', '3c_3']
    #categories = ['4c_1', '4c_2', '4c_3', '4c_4']
    #categories = ['5c_1', '5c_2', '5c_3', '5c_4', '5c_5']
    #categories = ['6c_1', '6c_2', '6c_3', '6c_4', '6c_5', '6c_6']
    #categories = ['short_support', 'short_wellness', 'short_RTI', 'short_parent']
    categories = ['cat1', 'cat2', 'cat3', 'cat5', 'cat6', 'cat9', 'cat10', 'cat13', 'cat14']
    #categories = ['cat[1, 3, 6, 9, 13]', 'cat[2, 9]', 'cat[1, 6, 10]', 'cat[5, 9, 14]', 'cat[6, 9]']
    #categories = ['cat[1, 3, 6, 9, 13]', 'cat[1, 6, 10]', 'cat[2, 9]', 'cat[5, 9, 14]', 'cat[6]', 'cat[9]']

    #categories = ['cat[1, 3, 6, 9, 13]', 'cat[1, 6, 10]', 'cat[2, 9]', 'cat[5, 14]', 'cat[6]', 'cat[9]']


    if len(argv) == 1:
        train(categories)
        classify(categories)
    elif (argv[1] == 'train'):
        train(categories)
    elif (argv[1] == 'classify'):
        classify(categories)
    elif (argv[1] == 'nc'):
        train_nc(categories)
        classify_nc(categories)

if __name__ == "__main__":
    main(sys.argv)
