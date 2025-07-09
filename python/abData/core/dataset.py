"""Manage the dataset for the asset pipeline."""
import abJSON
from pprint import pprint
from config import PipePaths


def compose_dataset(data):
    """Composes the dataset with the provided data."""
    current_data = abJSON.read(PipePaths.DATASET.value)

    if not validate_data([data])[0]:
        raise ValueError("Data validation failed. Please check the data against the template.")

    current_data.append(data)
    abJSON.write(PipePaths.DATASET.value, current_data)


def get_dataset() -> dict:
    """Retrieves the current dataset."""
    return abJSON.read(PipePaths.DATASET.value)


def validate_dataset() -> tuple[bool, bool, list[tuple], list[tuple]]:
    """
    Validates the dataset against the template.
    Ensures all keys are present and values are not the default values from the template.

    Returns:
        Tuple(is_valid, is_empty, missing_keys, defaulted_keys)
    """
    dataset = abJSON.read(PipePaths.DATASET.value)
    return validate_data(dataset)


def validate_data(dataset):
    template = abJSON.read(PipePaths.TEMPLATE.value)
    missing_keys = []
    defaulted_keys = []

    for i, item in enumerate(dataset):
        for key, default_value in template.items():
            if key not in item:
                missing_keys.append((i, key))
            elif item[key] == default_value:
                defaulted_keys.append((i, key))

    is_empty = not dataset
    is_valid = not is_empty and not missing_keys and not defaulted_keys
    return is_valid, is_empty, missing_keys, defaulted_keys


def print_dataset():
    """Prints the current dataset."""
    pprint("Current Dataset:")
    pprint(abJSON.read(PipePaths.DATASET.value))


def reset_dataset():
    """Resets the dataset to an empty state."""
    abJSON.write(PipePaths.DATASET.value, {})
    