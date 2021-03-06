#!/usr/bin/env python3
import os

import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score

from embedding_evaluation.load_embedding import load_embedding_textfile


def process_concreteness():
    dataset_path = './embedding_evaluation/data/usf/concreteness.txt'

    concreteness = {}
    with open(dataset_path, "r") as f:
        data = f.read().splitlines()

    for line in data:
        s = line.split(",")
        concreteness[s[0]] = float(s[1])
    return concreteness


def evaluate_one_dataset(labels, features, rerun=2):
    scores = []
    for i in range(rerun):
        clf = SVR(kernel="rbf")
        score = cross_val_score(clf, features, labels, cv=5)#, scoring="f1")
        #print(score)
        scores.extend(score)
    return scores

class EvaluationConcreteness:

    def __init__(self, entity_subset=None):
        self.concreteness = process_concreteness()

    def words_in_benchmarks(self):
        vocab = set(self.concreteness.keys())
        return vocab

    def evaluate(self, my_embedding):
        labels = []
        features = []
        words_with_embedding = 0
        for word, conc in self.concreteness.items():
            if word in my_embedding:
                words_with_embedding += 1
                labels.append(conc)
                features.append(my_embedding[word])
                #features.append(np.random.randn(300))
        #print("Evaluated words: %d" % len(labels))

        features = np.array(features)
        scores = evaluate_one_dataset(labels, features)
        mean = np.mean(scores)
        std = np.std(scores)
        results = {"mean": mean, "std": std, "total_words" : len(self.concreteness), "words_with_embedding" : words_with_embedding}

        return results

