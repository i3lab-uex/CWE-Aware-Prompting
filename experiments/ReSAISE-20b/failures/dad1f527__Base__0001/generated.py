import json
import pickle
from pathlib import Path
from typing import Any, Dict, Type

# Whitelisted formats
ALLOWED_FORMATS = {"json", "text", "pickle"}

# Allowed types for pickle deserialization
ALLOWED_PICKLE_TYPES: Dict[str, Type] = {
    "int": int,
    "float": float,
    "str": str,
    "bytes": bytes,
    "list": list,
    "tuple": tuple,
    "dict": dict,
    "set": set,
}


class RestrictedUnpickler(pickle.Unpickler):
    """
    A restricted unpickler that only allows a predefined set of built-in types.
    """

    def find_class(self, module: str, name: str) -> Any:
        # Only allow built-in types from the whitelist
        if module == "builtins" and name in ALLOWED_PICKLE_TYPES:
            return ALLOWED_PICKLE_TYPES[name]
        raise pickle.UnpicklingError(
            f"Attempted to unpickle disallowed class {module}.{name}"
        )


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load and deserialize data from a file using a whitelisted format.

    Parameters
    ----------
    filepath : str
        Path to the serialized file.
    data_format : str
        The format of the serialized data. Must be one of ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    if data_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(
            f"Untrusted or unsupported data format: {data_format!r}. "
            f"Allowed formats are: {', '.join(sorted(ALLOWED_FORMATS))}"
        )

    path = Path(filepath)
    if not path.is_file():
        raise ValueError(f"File does not exist: {filepath!r}")

    try:
        with path.open("rb") as f:
            raw = f.read()
    except OSError as exc:
        raise ValueError(f"Unable to read file {filepath!r}: {exc}") from exc

    if data_format.lower() == "json":
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to parse JSON: {exc}") from exc

    if data_format.lower() == "text":
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Failed to decode text: {exc}") from exc

    if data_format.lower() == "pickle":
        try:
            # Use restricted unpickler to mitigate CWE‑502
            return RestrictedUnpickler(io.BytesIO(raw)).load()
        except (pickle.UnpicklingError, EOFError) as exc:
            raise ValueError(f"Failed to unpickle data: {exc}") from exc