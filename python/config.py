"""Configuration for the asset processing pipeline."""
import os
import enum


class PipePaths(enum.Enum):
    """Paths for the asset processing pipeline."""

    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA = os.path.join(ROOT, "data")
    IN = os.path.join(DATA, "in")
    OUT = os.path.join(DATA, "out")
    HDAS = os.path.join(ROOT, "hdas")
    ARCHIVES = os.path.join(DATA, "archives")
    DATASET = os.path.join(DATA, "dataset.json")
    TEMPLATE = os.path.join(DATA, "template.json")

    def __str__(self):
        return self.value
