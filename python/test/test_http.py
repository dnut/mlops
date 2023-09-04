from dataclasses import dataclass, asdict
import requests

from animal_classifier.common import AnimalClass, AnimalDescription
from animal_classifier.client import AnimalClassifierClient

if __name__ == "__main__":
    classify = AnimalClassifierClient("http://localhost:5000").classify_animal

    aardvark = AnimalDescription(1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 0, 0, 1)
    frog = AnimalDescription(0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 4, 0, 0, 0)

    mammal = AnimalClass(1, "Mammal")
    amphibian = AnimalClass(5, "Amphibian")

    assert mammal == classify(aardvark)
    assert amphibian == classify(frog)

    print("test passed")

    # TODO: convert this into something that can run in pytest with a fixture to
    # start the flask server. also needs to remain runnable against arbitrary
    # pre-existing servers, such as a docker container.
