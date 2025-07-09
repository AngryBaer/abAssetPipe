import os
import pytest

from .. import config


def test_pipepaths_values():
    root = os.path.dirname(os.path.dirname(os.path.abspath(config.__file__)))
    assert config.PipePaths.ROOT.value == root
    assert config.PipePaths.DATA.value == os.path.join(root, "data")
    assert config.PipePaths.IN.value == os.path.join(root, "data", "in")
    assert config.PipePaths.OUT.value == os.path.join(root, "data", "out")
    assert config.PipePaths.HDAS.value == os.path.join(root, "hdas")
    assert config.PipePaths.ARCHIVES.value == os.path.join(root, "data", "archives")
    assert config.PipePaths.DATASET.value == os.path.join(root, "data", "dataset.json")
    assert config.PipePaths.TEMPLATE.value == os.path.join(root, "data", "template.json")

def test_pipepaths_str():
    assert str(config.PipePaths.ROOT) == config.PipePaths.ROOT.value
    assert str(config.PipePaths.DATA) == config.PipePaths.DATA.value
