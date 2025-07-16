"""Classify assets into units of data that can be used for machine learning."""
import os
import numpy
import open3d
import abJSON

from config import PipePaths


class Asset():
    """Represents an asset in the abData package, backed by template.json structure."""

    def __init__(self, i: str, data: dict):
        template = abJSON.read(PipePaths.TEMPLATE.value)

        # Initialize the asset by filling only the keys present in the template
        self._data_in = data
        self._data = {**template, **{k: v for k, v in data.items() if k in template}}

        # Ensure the asset has an ID and a valid path
        self.id = i
        self.path = os.path.join(PipePaths.IN.value, data["file"])

        # Initialize mesh instance to None, will be loaded when needed
        self._mesh = None

    def __str__(self) -> str:
        """String representation of the asset."""
        return f"Asset(id={self.id}, name={self.name}, points={self.count})"

    def __repr__(self) -> str:
        """Representation of the asset."""
        return str(self._data)

    @property
    def data(self) -> dict:
        """Get the asset data."""
        return self._data

    @property
    def data_in(self) -> dict:
        """Get the original asset data input."""
        return self._data_in

    @property
    def id(self) -> str:
        """Get or set the asset ID."""
        return self._data["id"]

    @id.setter
    def id(self, value):
        self._data["id"] = value

    @property
    def name(self) -> str:
        """Get or set the asset name."""
        return self._data["name"]

    @name.setter
    def name(self, value):
        self._data["name"] = value

    @property
    def description(self) -> str:
        """This is a brief description of the asset."""
        return self._data["description"]

    @description.setter
    def description(self, value):
        self._data["description"] = value

    @property
    def path(self) -> os.PathLike:
        """Get the asset path."""
        return self._data["path"]

    @path.setter
    def path(self, value):
        """Set the asset path to a valid path in the system."""
        if not os.path.exists(value):
            raise FileNotFoundError(f"Path for asset {self} does not exist: {value}")

        self._data["path"] = value

    @property
    def count(self) -> int:
        """Get or set the polygon count."""
        return self._data["count"]

    @count.setter
    def count(self, value):
        self._data["count"] = value

    @property
    def bbox(self) -> list:
        """Get or set the bounding box of the asset."""
        return self._data["bbox"]

    @bbox.setter
    def bbox(self, value):
        self._data["bbox"] = value

    @property
    def volume(self) -> float:
        """Get or set the volume of the asset."""
        return self._data.get("volume", 0.0)

    @volume.setter
    def volume(self, value):
        self._data["volume"] = value

    @property
    def watertight(self) -> bool:
        """Get or set the watertight status of the asset."""
        return self._data.get("watertight", False)

    @watertight.setter
    def watertight(self, value: bool):
        self._data["watertight"] = value

    @property
    def tags(self) -> list:
        """Get or set the tags associated with the asset."""
        return self._data["tags"]

    @tags.setter
    def tags(self, value):
        self._data["tags"] = value

    @property
    def type(self) -> str:
        """Get or set the type of the asset."""
        return self._data.get("type", "")

    @type.setter
    def type(self, value):
        self._data["type"] = value

    @property
    def file(self) -> str:
        """Get or set the file associated with the asset."""
        return self._data.get("file", "")

    @file.setter
    def file(self, value):
        self._data["file"] = value

    def add_tag(self, tag: str):
        """Add a tag to the asset."""
        if tag not in self._data["tags"]:
            self._data["tags"].append(tag)

    def load_mesh(self):
        """Loads the mesh from the asset path."""
        if self._mesh is None:
            self._mesh = open3d.io.read_triangle_mesh(self.path, enable_post_processing=True)

    def get_point_count(self) -> int:
        """Extracts the point count from the asset geometry."""
        self.load_mesh()

        self.count = len(numpy.asarray(self._mesh.vertices))
        return self.count

    def get_bounding_box(self) -> list:
        """Extracts the bounding box from the asset geometry."""
        self.load_mesh()

        bbox_o = self._mesh.get_oriented_bounding_box()
        points = bbox_o.get_box_points()
        self.bbox = numpy.asarray(points).tolist()
        return self.bbox


def iter_database_json(name: str):
    """Iterates over the database JSON file for the given name.

    Yields:
        Asset: An instance of the Asset class for each entry in the database.
    """
    assets = abJSON.read(os.path.join(PipePaths.ARCHIVES.value, f"{name}.json"))
    for i, data in assets.items():
        yield Asset(i, data)
