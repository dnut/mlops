import os
import logging
import sys

from animal_classifier.app import classification_server
from animal_classifier.common import load_class_id_to_name, try_dotenv
from animal_classifier.sklearn import SkLearnAnimalClassifier, load_pickled_clf

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
try_dotenv()
classes = load_class_id_to_name(os.environ["CLASS_FILE_PATH"])
clf = load_pickled_clf(os.environ["SKLEARN_PICKLE_PATH"])

app = classification_server(SkLearnAnimalClassifier(clf, classes))

if __name__ == "__main__":
    app.run()
