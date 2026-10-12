import json
import pickle
from typing import Any, Set


# Define the whitelist of supported formats
ALLOWED_FORMATS: Set[str] = {"json", "text", "pickle"}


class SafeUnpickler(pickle.Unpickler):
    """
    A custom Unpickler that only allows built‑in types to be instantiated.
    This mitigates the risk of executing arbitrary code during unpickling
    (CWE‑502).
    """
    # Whitelist of fully qualified names for built‑in types
    _ALLOWED_BUILTINS = {
        "builtins.list",
        "builtins.dict",
        "builtins.tuple",
        "builtins.set",
        "builtins.frozenset",
        "builtins.int",
        "builtins.float",
        "builtins.str",
        "builtins.bytes",
        "builtins.bool",
        "builtins.NoneType",  # used for None
    }

    def find_class(self, module: str, name: str):
        fullname = f"{module}.{name}"
        if fullname not in self._ALLOWED_BUILTINS:
            raise pickle.UnpicklingError(
                f"Attempted to unpickle disallowed type: {fullname}"
            )
        return super().find_class(module, name)


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load and deserialize data from a file using only trusted formats.

    Parameters
    ----------
    filepath : str
        Path to the serialized file.
    data_format : str
        Format of the serialized data. Must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist or if an unsafe pickle
        payload is encountered.
    FileNotFoundError
        If the file does not exist.
    """
    if data_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(
            f"Untrusted or unsupported format '{data_format}'. "
            f"Allowed formats: {', '.join(sorted(ALLOWED_FORMATS))}"
        )

    with open(filepath, "rb") as fh:
        if data_format.lower() == "json":
            # JSON files are typically text; read as UTF‑8
            return json.load(fh)
        elif data_format.lower() == "text":
            # Return raw text content as a string
            return fh.read().decode("utf-8")
        elif data_format.lower() == "pickle":
            # Use the safe unpickler
            try:
                return SafeUnpickler(fh).load()
            except pickle.UnpicklingError as exc:
                raise ValueError(
                    f"Unsafe or corrupted pickle data: {exc}"
                ) from exc
        else:
            # This block should never be reached due to the whitelist check.
            raise ValueError(f"Unhandled format: {data_format}")