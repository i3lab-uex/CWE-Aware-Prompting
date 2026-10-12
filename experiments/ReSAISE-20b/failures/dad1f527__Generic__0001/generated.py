import json
import pickle
from pathlib import Path
from typing import Any


class SafeUnpickler(pickle.Unpickler):
    """
    A custom unpickler that only allows built‑in classes and functions.
    This reduces the risk of executing malicious code during unpickling.
    """

    def find_class(self, module: str, name: str):
        # Only allow built‑in modules
        if module != "builtins":
            raise pickle.UnpicklingError(
                f"Attempted to load disallowed class {module}.{name}"
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
        One of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist.
    """
    # Whitelist of supported formats
    SUPPORTED_FORMATS = {"json", "text", "pickle"}

    if data_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Untrusted or unsupported data format: {data_format!r}. "
            f"Supported formats are: {', '.join(sorted(SUPPORTED_FORMATS))}."
        )

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {filepath!r}")

    if data_format == "json":
        with path.open("rt", encoding="utf-8") as f:
            return json.load(f)

    if data_format == "text":
        with path.open("rt", encoding="utf-8") as f:
            return f.read()

    # data_format == "pickle"
    with path.open("rb") as f:
        return SafeUnpickler(f).load()