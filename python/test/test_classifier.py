import os

from animal_classifier.common import AnimalClassifier, AnimalDescription, load_class_id_to_name
from animal_classifier.onnx import AnimalClass, OnnxAnimalClassifier, load_onnx_session
from animal_classifier.sklearn import SkLearnAnimalClassifier, load_pickled_clf


def root_path(request, path: str):
    return os.path.join(request.config.rootdir, path)


def test_sklearn_classifier(request):
    classifier = SkLearnAnimalClassifier(
        load_pickled_clf(root_path(request, "animal-classes.pkl")),
        load_class_id_to_name(root_path(request, "input/class.csv")),
    )
    run_classifier_test(classifier)


def test_onnx_classifier(request):
    classifier = OnnxAnimalClassifier(
        load_onnx_session(root_path(request, "animal-classes.onnx")),
        load_class_id_to_name(root_path(request, "input/class.csv")),
    )
    run_classifier_test(classifier)


def run_classifier_test(classifier: AnimalClassifier):
    aardvark = AnimalDescription(1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 0, 0, 1)
    frog = AnimalDescription(0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 4, 0, 0, 0)

    mammal = AnimalClass(1, "Mammal")
    amphibian = AnimalClass(5, "Amphibian")

    assert mammal == classifier.classify_animal(aardvark)
    assert amphibian == classifier.classify_animal(frog)
