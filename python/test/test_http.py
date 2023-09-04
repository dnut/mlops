from dataclasses import dataclass, asdict
import requests

from animal_classifier.common import AnimalClass, AnimalDescription

if __name__ == '__main__':

    def classify(description: AnimalDescription) -> AnimalClass:
        response = requests.post("http://localhost:5000/classify", json=asdict(description))
        return AnimalClass(**response.json())


    aardvark = AnimalDescription(1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 0, 0, 1)
    frog = AnimalDescription(0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 4, 0, 0, 0)

    mammal = AnimalClass(1, "Mammal")
    amphibian = AnimalClass(5, "Amphibian")

    assert mammal == classify(aardvark)
    assert amphibian == classify(frog)

    print("test passed")

    # TODO: convert this into something that can run in pytest with a fixture to
    # start the flask server.
