#!/usr/bin/python
from subprocess import call
import sys

categories = ['dropout', 'parent', 'PBIS', 'RTI', 'support', 'teaming', 'health']

def train():
    for c in categories:
        call(["./svm_learn", c + "/" + c + "_train.dat", c + "/model"])

def classify():
    for c in categories:
        call(["./svm_classify", c + "/test.dat", c + "/model", c + "/predictions"])

def train_nc():
    for c in categories:
        call(["./svm_learn", c + "/train_nc.dat", c + "/model_nc"])

def classify_nc():
    for c in categories:
        call(["./svm_classify", c + "/test_nc.dat", c + "/model_nc", c + "/predictions_nc"])


def main(argv):
    if len(argv) == 1:
        train()
        classify()
    elif (argv[1] == 'train'):
        train()
    elif (argv[1] == 'classify'):
        classify()
    elif (argv[1] == 'nc'):
        train_nc()
        classify_nc()

if __name__ == "__main__":
    main(sys.argv)
