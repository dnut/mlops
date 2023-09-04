import csv
import logging
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Dict


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


@dataclass
class AnimalClass:
    class_id: int
    name: str


class AnimalClassifier(metaclass=ABCMeta):
    @abstractmethod
    def classify_animal(self, description: AnimalDescription) -> AnimalClass:
        pass


def load_class_id_to_name(class_csv_path: str) -> Dict[int, str]:
    with open(class_csv_path) as f:
        return {int(r["Class_Number"]): r["Class_Type"] for r in csv.DictReader(f)}


def try_dotenv():
    try:
        from dotenv import load_dotenv
        logging.info("using .env if available")
        load_dotenv()
    except:
        logging.info("not using .env")
