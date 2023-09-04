from sklearn import svm
from sklearn.model_selection import train_test_split
from skl2onnx import to_onnx
import pandas as pd
import pickle


def main():
    data = pd.read_csv('input/zoo.csv')
    all_X, all_y = preprocess(data)

    clf = train(all_X, all_y)

    # export pickle
    with open('animal-classes.pkl', 'wb') as f:
        pickle.dump(clf, f)

    # export onnx
    onx = to_onnx(clf, all_X.values)
    with open('animal-classes.onnx', 'wb') as f:
        f.write(onx.SerializeToString())


def train(all_X, all_y) -> svm.SVC:
    X_train, X_test, y_train, y_test = train_test_split(all_X, all_y)
    clf = svm.SVC()
    clf.fit(X_train.values, y_train)
    print(f'model trained with score: {clf.score(X_test, y_test)}')
    return clf


def preprocess(data):
    X = data.iloc[:, 1:17]  # all rows, all the features and no labels
    y = data.iloc[:, 17]  # all rows, label only
    return X, y


if __name__ == '__main__':
    main()
