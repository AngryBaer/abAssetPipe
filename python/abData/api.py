"""This module provides a an API for the abData package."""
from .core import assets, dataset


def run_metadata_pipeline(database_name: str):
    """Run the metadata pipeline."""
    for asset in assets.iter_database_json(database_name):
        asset.get_point_count()
        asset.get_bounding_box()
        asset.add_tag(asset.data_in["type"])

        print(asset)
        dataset.compose_dataset(asset.data)


def run_validation_pipeline():
    """Run the validation pipeline."""
    is_valid, is_empty, missing_keys, defaulted_keys = dataset.validate_dataset()

    if is_valid:
        print("Dataset is valid.")
    else:
        print("Dataset validation failed:")
        if is_empty:
            print("Dataset is empty.")
        for i, key in missing_keys:
            print(f"Item {i} is missing key: {key}")
        for i, key in defaulted_keys:
            print(f"Item {i} has default value for key: {key}")


def print_dataset():
    """Print the current dataset."""
    dataset.print_dataset()


def reset_dataset():
    """Reset the dataset to an empty state."""
    dataset.reset_dataset()
    print("Dataset has been reset.")
