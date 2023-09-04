from dataclasses import dataclass, astuple
from sklearn import svm
import pandas as pd
import pickle

from animal_classifier.common import AnimalClassifier, AnimalClass, AnimalDescription


@dataclass
class SkLearnAnimalClassifier(AnimalClassifier):
    clf: svm.SVC
    class_id_to_name: dict

    def classify_animal(self, description: AnimalDescription) -> AnimalClass:
        df = pd.DataFrame([astuple(description)])
        class_id = int(self.clf.predict(df)[0])
        name = self.class_id_to_name[class_id]
        return AnimalClass(class_id, name)


def load_pickled_clf(model_path: str) -> svm.SVC:
    with open(model_path, "rb") as f:
        return pickle.load(f)
