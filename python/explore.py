"""This file is a mess that was used for exploration. It mixes a bunch of code
that's currently split in different files under animal_classifier.
"""

import csv

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from dataclasses import dataclass, asdict, astuple
import pandas as pd
import numpy as np
from skl2onnx import to_onnx
import onnxruntime as rt


@dataclass
class AnimalDescription:
    hair: int
    feathers: int
    eggs: int
    milk: int
    airborne: int
    aquatic: int
    predator: int
    toothed: int
    backbone: int
    breathes: int
    venomous: int
    fins: int
    legs: int
    tail: int
    domestic: int
    catsize: int


def main():
    data = pd.read_csv("input/zoo.csv")
    all_X, all_y = preprocess(data)
    X_train, X_test, y_train, y_test = train_test_split(all_X, all_y)
    clf = svm.SVC()
    # clf = RandomForestClassifier()
    clf.fit(X_train.values, y_train)
    print(f'model trained with score: {clf.score(X_test, y_test)}')
    # test = clf.predict(X_test[15:25])
    # print(type(X_test[15:25]))
    # print(type(clf))
    # print(list(test))
    # print(list(y_test[15:25].array))

    aardvark = AnimalDescription(1,0,0,1,0,0,1,1,1,1,0,0,4,0,0,1)
    frog = AnimalDescription(0,0,1,0,0,1,1,1,1,1,1,0,4,0,0,0)
    with open("input/class.csv") as f:
        animal_class_id_to_name = {int(r['Class_Number']): r['Class_Type'] for r in csv.DictReader(f)}
    
    my_test = pd.DataFrame([asdict(aardvark)])
    print(animal_class_id_to_name[clf.predict(my_test)[0]])


    onx = to_onnx(clf, all_X.values)
    with open("animal-classes.onnx", "wb") as f:
        f.write(onx.SerializeToString())

    # onx = to_onnx(svm.SVC())
    # with open("animal-classes.onnx", "rb") as f:
    #     onx.ParseFromString(f.read())

    sess = rt.InferenceSession("animal-classes.onnx", providers=["CPUExecutionProvider"])
    print(type(sess))
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    print(input_name)
    # print([x.name for x in sess.get_inputs()])
    # pred_onx = sess.run([label_name], {input_name: X_test.astype(np.float32)})[0]
    # pred = sess.run([label_name], {k: np.array([[v]]).astype(np.int64) for k, v in asdict(aardvark).items()})
    pred = sess.run([label_name], {input_name: np.array([astuple(aardvark)]).astype(np.int64)})
    print(pred)
    pred = sess.run([label_name], {input_name: np.array([astuple(frog)]).astype(np.int64)})
    print(pred)
    

def preprocess(data):
    X = data.iloc[:, 1:17] # all rows, all the features and no labels
    y = data.iloc[:, 17]   # all rows, label only
    return X, y


if __name__ == '__main__':
    main()
