from flask import Flask, request
from dataclasses import asdict

from animal_classifier.common import AnimalClassifier, AnimalDescription


def classification_server(classifier: AnimalClassifier):
    app = Flask(f'animal classification server using {type(classifier)}')

    @app.route('/classify', methods=['POST'])
    def classify_animal():
        req = AnimalDescription(**request.get_json())
        response = classifier.classify_animal(req)
        return asdict(response)

    return app
