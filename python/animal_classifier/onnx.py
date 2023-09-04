from dataclasses import astuple
import onnxruntime
import numpy as np

from animal_classifier.common import AnimalClassifier, AnimalClass, AnimalDescription


class OnnxAnimalClassifier(AnimalClassifier):
    def __init__(
        self, inference_session: onnxruntime.InferenceSession, class_id_to_name: dict
    ):
        self._inference_session = inference_session
        self._input_name = inference_session.get_inputs()[0].name
        self._label_name = inference_session.get_outputs()[0].name
        self._class_id_to_name = class_id_to_name

    def classify_animal(self, description: AnimalDescription) -> AnimalClass:
        class_id = self._inference_session.run(
            [self._label_name],
            {self._input_name: np.array([astuple(description)]).astype(np.int64)},
        )
        return AnimalClass(int(class_id[0][0]), self._class_id_to_name[class_id[0][0]])


def load_onnx_session(onnx_file_path: str) -> onnxruntime.InferenceSession:
    return onnxruntime.InferenceSession(
        onnx_file_path, providers=["CPUExecutionProvider"]
    )
