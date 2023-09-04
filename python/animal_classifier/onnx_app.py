import os

from animal_classifier.app import classification_server
from animal_classifier.common import load_class_id_to_name, try_dotenv
from animal_classifier.onnx import OnnxAnimalClassifier, load_onnx_session

try_dotenv()

ort = load_onnx_session(os.environ["ONNX_FILE_PATH"])
classes = load_class_id_to_name(os.environ["CLASS_FILE_PATH"])

app = classification_server(OnnxAnimalClassifier(ort, classes))

if __name__ == "__main__":
    app.run()
