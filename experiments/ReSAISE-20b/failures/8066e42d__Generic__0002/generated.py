import json
import pickle
from pathlib import Path
from typing import Any

# A whitelist of safe serialization formats.
_SAFE_FORMATS = {"json", "text", "pickle"}

# If you want to restrict pickle further, define a whitelist of allowed classes.
_ALLOWED_PICKLE_MODULES = {"builtins", "datetime"}


def _safe_unpickler(file_obj) -> Any:
    """
    Load a pickle object from *file_obj* while restricting the classes that can be
    instantiated. Only objects whose class is defined in *_ALLOWED_PICKLE_MODULES*
    are allowed; all others raise a ValueError.
    """
    class RestrictedUnpickler(pickle.Unpickler):
        def find_class(self, module: str, name: str):
            if module not in _ALLOWED_PICKLE_MODULES:
                raise pickle.UnpicklingError(
                    f"Attempting to load unsafe module '{module}'."
                )
            return super().find_class(module, name)

    return RestrictedUnpickler(file_obj).load()


def deserialize_file_data(filepath: str, serialization_format: str) -> Any:
    """
    Deserialize data from *filepath* using the specified *serialization_format*.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    serialization_format : str
        One of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *serialization_format* is not in the safe list.
    """
    if serialization_format not in _SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: {serialization_format!r}. "
            f"Allowed formats are: {_SAFE_FORMATS}"
        )

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {filepath!r}")

    if serialization_format == "json":
        with path.open("rt", encoding="utf-8") as f:
            return json.load(f)

    if serialization_format == "text":
        with path.open("rt", encoding="utf-8") as f:
            return f.read()

    if serialization_format == "pickle":
        with path.open("rb") as f:
            return _safe_unpickler(f)

    # This line should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization format: {serialization_format!r}")