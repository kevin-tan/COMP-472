# Task 0: you first need to remove the document identifier, and also the topic label, which you don't need.
# Then, split the data into a training and an evaluation part. For instance, we may use 80% for training and the
# remainder for evaluation.

def read_documents(path):
    f = open(path, "r", encoding="utf8")
    all_labels = []
    all_documents = []
    for word in f:
        word = word.replace('\n', '').replace('\t', '')
        list_words = word.split(" ")
        all_labels.append(list_words[1])
        all_documents.append(" ".join(list_words[3:]))
    return all_documents, all_labels


file_path_name = "all_sentiment_shuffled"
all_docs, all_labels = read_documents('data/{file_path_name}.txt'.format(file_path_name=file_path_name))
split_point = int(0.80 * len(all_docs))
train_docs = all_docs[:split_point]
train_labels = all_labels[:split_point]
eval_docs = all_docs[split_point:]
eval_labels = all_labels[split_point:]

# Task 1: Plot the distribution of the number of the instances in each class.

import matplotlib.pyplot as plt


def plot_data(labels):
    labels_counts = dict()
    for label in labels:
        labels_counts[label] = labels_counts.get(label, 0) + 1
    plt.bar(labels_counts.keys(), labels_counts.values())
    plt.show()


plot_data(train_labels)
plot_data(eval_labels)

# Task 2: Run 3 different ML models:
# a) Naive Bayes Classifier
# b) Base-DT: a baseline Decision Tree using entropy as decision criterion and using default values for
# the rest of the parameters.
# c) Best-DT: a better performing Decision Tree

from sklearn.feature_extraction.text import TfidfVectorizer


def data_vectorizer(training_data):
    vect = TfidfVectorizer()
    return vect.fit(training_data)


from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import numpy as np


def predict_with_classifier(classifier, generated_path, train_X, train_Y, test_X, test_Y):
    classifier.fit(train_X, train_Y)
    y_pred = classifier.predict(test_X)
    with open(generated_path, "a") as f:
        f.write(np.array2string(classifier.classes_, separator=', '))
        f.write("\n")
        for i in range(len(y_pred)):
            f.write("%d, %d\n" % (i, classifier.classes_.tolist().index(y_pred[i])))
        f.write(
            "Confusion matrix %s\n" % (np.array2string(confusion_matrix(y_true=test_Y, y_pred=y_pred), separator=', ')))
        f.write("Precision score: %s\nRecall score: %s\nF1 score: %s\n" % (
            precision_score(y_true=test_Y, y_pred=y_pred, average=None),
            recall_score(y_true=test_Y, y_pred=y_pred, average=None),
            f1_score(y_true=test_Y, y_pred=y_pred, average=None)))
        f.write("Accuracy score: %f" % (accuracy_score(y_true=test_Y, y_pred=y_pred)))


# Vectorize String data into frequency count
vectorizer = data_vectorizer(train_docs)
train_X = vectorizer.transform(train_docs)
test_X = vectorizer.transform(eval_docs)

# Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB

predict_with_classifier(MultinomialNB(),
                        "result/MultinomialNaiveBayes-{file_path_name}.txt".format(file_path_name=file_path_name),
                        train_X,
                        train_labels, test_X, eval_labels)

# Base-DT: a baseline Decision Tree using entropy as decision criterion and using default values for the rest of the
# parameters.
from sklearn.tree import DecisionTreeClassifier

predict_with_classifier(DecisionTreeClassifier(criterion='entropy'),
                        "result/defaultBaseDT-{file_path_name}.txt".format(file_path_name=file_path_name), train_X,
                        train_labels,
                        test_X,
                        eval_labels)

# Best-DT: a better performing Decision Tree with random params using GridSearchCV
from sklearn.model_selection import GridSearchCV


def find_best_dt_with_params(train_X, train_Y):
    base_classifier = DecisionTreeClassifier()
    params_grid = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [None, 3, 5, 10],
        'min_samples_split': [10, 25, 50, 75],
        'min_impurity_decrease': [0.0, 0.1, 0.2, 0.3],
        'class_weight': [None, 'balanced']
    }
    grid_search = GridSearchCV(base_classifier, param_grid=params_grid, cv=5).fit(train_X, train_Y)
    return grid_search.best_estimator_


predict_with_classifier(find_best_dt_with_params(train_X, train_labels),
                        "result/improvedBaseDT-{file_path_name}.txt".format(file_path_name=file_path_name), train_X,
                        train_labels, test_X,
                        eval_labels)
