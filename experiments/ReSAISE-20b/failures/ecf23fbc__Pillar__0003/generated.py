import json
import pickle
from pickle import Unpickler, PickleError
from typing import Any


class RestrictedUnpickler(Unpickler):
    """
    A minimal safe unpickler that only allows built‑in container types and
    primitive data. Any attempt to load a custom class or module raises an
    exception.
    """

    # Whitelist of allowed (module, name) tuples
    _allowed = {
        ("builtins", "dict"),
        ("builtins", "list"),
        ("builtins", "tuple"),
        ("builtins", "set"),
        ("builtins", "frozenset"),
        ("builtins", "str"),
        ("builtins", "bytes"),
        ("builtins", "int"),
        ("builtins", "float"),
        ("builtins", "bool"),
        ("builtins", "NoneType"),
    }

    def find_class(self, module: str, name: str):
        if (module, name) not in self._allowed:
            raise pickle.UnpicklingError(
                f"Attempt to unpickle disallowed class {module}.{name}"
            )
        return super().find_class(module, name)


def interpret_serialized_content(src_file: str, content_type: str) -> Any:
    """
    Safely deserialize a file based on the provided content type.

    Parameters
    ----------
    src_file : str
        Path to the file to be deserialized.
    content_type : str
        Serialization format. Must be one of the trusted formats:
        'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    allowed_formats = {"json", "text", "pickle"}
    if content_type not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe format: {content_type}")

    with open(src_file, "rb") as f:
        if content_type == "json":
            # JSON is text based; read bytes and decode
            try:
                data = f.read().decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("JSON file is not UTF-8 encoded") from exc
            return json.loads(data)

        elif content_type == "text":
            try:
                return f.read().decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("Text file is not UTF-8 encoded") from exc

        elif content_type == "pickle":
            try:
                return RestrictedUnpickler(f).load()
            except PickleError as exc:
                raise ValueError("Failed to safely unpickle data") from exc