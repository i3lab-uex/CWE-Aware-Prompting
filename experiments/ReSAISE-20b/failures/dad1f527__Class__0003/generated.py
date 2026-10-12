import json
import pickle
from pathlib import Path
from typing import Any, Iterable

# A minimal restricted unpickler that only allows safe built‑in types.
class RestrictedUnpickler(pickle.Unpickler):
    """
    Unpickles data but only permits a limited set of safe built‑in classes.
    This mitigates the risk of arbitrary code execution (CWE‑913).
    """
    # Whitelist of allowed class names
    _allowed_builtins: Iterable[str] = {
        "list",
        "dict",
        "tuple",
        "set",
        "frozenset",
        "int",
        "float",
        "bool",
        "str",
        "bytes",
        "NoneType",
    }

    def find_class(self, module: str, name: str):
        if module == "builtins" and name in self._allowed_builtins:
            return getattr(pickle, module).__dict__[name]
        raise pickle.UnpicklingError(f"Disallowed pickle object: {module}.{name}")


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load serialized data from *filepath* according to the specified *data_format*.

    Supported formats (whitelisted):
        - 'json'  : JSON text
        - 'text'  : Plain text (returned as a string)
        - 'pickle': Pickle data, but only if it contains safe built‑in types

    Raises:
        ValueError: If *data_format* is not in the whitelist.
        pickle.UnpicklingError: If a disallowed object type is encountered during
                               unpickling.

    Returns:
        The deserialized Python object.
    """
    # Normalise the format string
    fmt = data_format.lower()

    if fmt not in {"json", "text", "pickle"}:
        raise ValueError(f"Untrusted or unsupported format: {data_format}")

    path = Path(filepath)

    if fmt == "json":
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)

    if fmt == "text":
        with path.open("r", encoding="utf-8") as fp:
            return fp.read()

    # fmt == "pickle"
    with path.open("rb") as fp:
        return RestrictedUnpickler(fp).load()