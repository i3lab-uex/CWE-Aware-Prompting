import json
import pickle
from pathlib import Path
from typing import Any

# ----------------------------------------------------------------------
# Restricted Unpickler (CWE-664 mitigation)
# ----------------------------------------------------------------------
class _RestrictedUnpickler(pickle.Unpickler):
    """
    A pickle.Unpickler that only allows a whitelist of safe built‑in types.
    All other classes raise an exception during deserialization.
    """

    # Whitelist of allowed built‑in types
    _ALLOWED_BUILTINS = {
        "dict",
        "list",
        "tuple",
        "set",
        "frozenset",
        "int",
        "float",
        "str",
        "bool",
        "NoneType",
    }

    def find_class(self, module: str, name: str):
        """
        Override to restrict class resolution.
        Only allow built‑in types from the whitelist.
        """
        if module == "builtins" and name in self._ALLOWED_BUILTINS:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(
            f"Attempt to unpickle disallowed class {module}.{name}"
        )


def _restricted_loads(data: bytes) -> Any:
    """
    Safely load pickle data using the restricted unpickler.
    """
    return _RestrictedUnpickler(
        io.BytesIO(data)
    ).load()


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def interpret_serialized_content(src_file: str, content_type: str) -> Any:
    """
    Deserialize data from a file in a secure manner.

    Parameters
    ----------
    src_file : str
        Path to the file containing serialized data.
    content_type : str
        Serialization format: 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the content_type is unsupported or unsafe.
    """
    # Normalise and validate format
    allowed_types = {"json", "text", "pickle"}
    fmt = content_type.lower()
    if fmt not in allowed_types:
        raise ValueError(f"Unsupported or unsafe content type: {content_type!r}")

    path = Path(src_file)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {src_file}")

    # Read and deserialize
    if fmt == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if fmt == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    # fmt == "pickle"
    with path.open("rb") as f:
        data = f.read()
    # Use restricted unpickler to avoid arbitrary code execution
    return _restricted_loads(data)


# ----------------------------------------------------------------------
# Example usage (uncomment for testing)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     obj = interpret_serialized_content("data.json", "json")
#     print(obj)