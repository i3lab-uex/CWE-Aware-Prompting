import json
import pickle
from pathlib import Path
from typing import Any


class RestrictedUnpickler(pickle.Unpickler):
    """
    A custom Unpickler that only allows a predefined set of safe classes.
    This mitigates the risk of executing arbitrary code during unpickling.
    """
    # Define a whitelist of safe modules and classes
    SAFE_CLASSES = {
        ('builtins', 'list'),
        ('builtins', 'dict'),
        ('builtins', 'tuple'),
        ('builtins', 'set'),
        ('builtins', 'int'),
        ('builtins', 'float'),
        ('builtins', 'str'),
        ('builtins', 'bool'),
    }

    def find_class(self, module: str, name: str):
        if (module, name) not in self.SAFE_CLASSES:
            raise pickle.UnpicklingError(
                f"Attempting to unpickle unsafe class {module}.{name}"
            )
        return super().find_class(module, name)


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load and deserialize data from a file in a secure manner.

    Parameters
    ----------
    filepath : str
        Path to the serialized file.
    data_format : str
        The format of the serialized data. Must be one of:
        - 'json'
        - 'text'   (plain text)
        - 'pickle'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is not in the whitelist.
    """
    # Whitelist of allowed formats
    ALLOWED_FORMATS = {"json", "text", "pickle"}
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {data_format}")

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File does not exist: {filepath}")

    if fmt == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if fmt == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    if fmt == "pickle":
        with path.open("rb") as f:
            # Use the restricted unpickler to avoid arbitrary code execution
            return RestrictedUnpickler(f).load()