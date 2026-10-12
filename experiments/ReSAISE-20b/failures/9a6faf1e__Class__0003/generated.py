import json
import pickle
from pathlib import Path
from typing import Any, Set


# ----------------------------------------------------------------------
# Safe unpickler that restricts the classes that can be loaded
# ----------------------------------------------------------------------
class RestrictedUnpickler(pickle.Unpickler):
    """
    A pickle Unpickler that only allows a predefined set of built‑in types.
    Any attempt to load other classes will raise an UnpicklingError.
    """
    # Whitelist of safe built‑in types
    SAFE_BUILTINS: Set[str] = {
        "str",
        "int",
        "float",
        "bool",
        "list",
        "tuple",
        "dict",
        "set",
    }

    def find_class(self, module: str, name: str):
        if module == "builtins" and name in self.SAFE_BUILTINS:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(
            f"Attempted to load unsafe class {module}.{name}"
        )


def safe_load_pickle(data: bytes) -> Any:
    """
    Load pickle data using RestrictedUnpickler.
    """
    return RestrictedUnpickler(io.BytesIO(data)).load()


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def read_serialized_file(file_path: str, file_format: str) -> Any:
    """
    Read a serialized file and return the deserialized Python object.

    Parameters
    ----------
    file_path : str
        Path to the serialized data file.
    file_format : str
        Serialization format. Must be one of the trusted formats:
        'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is not in the whitelist or if the file
        cannot be read.
    """
    # Define a whitelist of safe formats
    TRUSTED_FORMATS = {"json", "text", "pickle"}

    if file_format not in TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: {file_format}"
        )

    path = Path(file_path)
    if not path.is_file():
        raise ValueError(f"File does not exist: {file_path}")

    try:
        if file_format == "json":
            with path.open("r", encoding="utf-8") as fp:
                return json.load(fp)

        elif file_format == "text":
            with path.open("r", encoding="utf-8") as fp:
                return fp.read()

        elif file_format == "pickle":
            with path.open("rb") as fp:
                data = fp.read()
            # Use the restricted unpickler
            return safe_load_pickle(data)

    except (json.JSONDecodeError, pickle.UnpicklingError) as exc:
        raise ValueError(f"Failed to deserialize {file_format} data: {exc}") from exc
    except OSError as exc:
        raise ValueError(f"IO error while reading {file_path}: {exc}") from exc