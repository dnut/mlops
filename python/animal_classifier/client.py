from dataclasses import asdict, dataclass

import requests

from animal_classifier.common import AnimalClass, AnimalClassifier, AnimalDescription


@dataclass
class AnimalClassifierClient(AnimalClassifier):
    host: str

    def classify_animal(self, description: AnimalDescription) -> AnimalClass:
        response = requests.post(f"{self.host}/classify", json=asdict(description))
        return AnimalClass(**response.json())
