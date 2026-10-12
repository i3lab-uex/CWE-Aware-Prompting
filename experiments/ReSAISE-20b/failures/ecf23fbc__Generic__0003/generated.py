import json
import pickle
from pathlib import Path
from typing import Any


class SafeUnpickler(pickle.Unpickler):
    """
    Unpickler that only allows objects from a whitelist of modules/classes.
    By default, it permits only built-in types and the 'datetime' module.
    """

    # Whitelisted modules and classes (module, class name)
    _whitelist = {
        ('builtins', 'list'),
        ('builtins', 'dict'),
        ('builtins', 'tuple'),
        ('builtins', 'set'),
        ('builtins', 'frozenset'),
        ('builtins', 'int'),
        ('builtins', 'float'),
        ('builtins', 'str'),
        ('builtins', 'bytes'),
        ('builtins', 'bool'),
        ('datetime', 'datetime'),
    }

    def find_class(self, module: str, name: str):
        if (module, name) in self._whitelist:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(
            f"Disallowed pickle object: {module}.{name}"
        )


def interpret_serialized_content(src_file: str, content_type: str) -> Any:
    """
    Deserialize data from *src_file* safely based on the specified *content_type*.

    Supported formats (case-insensitive):
        - 'json'   : JSON-encoded data.
        - 'text'   : Plain text; returned as a string.
        - 'pickle' : Pickled data, but only allows objects from the whitelist.

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
        If the format is unsupported or unsafe.
    """
    # Normalize content_type and validate
    fmt = content_type.strip().lower()
    if fmt not in {"json", "text", "pickle"}:
        raise ValueError(f"Unsupported or unsafe content type: {content_type}")

    path = Path(src_file)
    if not path.is_file():
        raise FileNotFoundError(f"File does not exist: {src_file}")

    if fmt == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if fmt == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    # fmt == "pickle"
    with path.open("rb") as f:
        try:
            return SafeUnpickler(f).load()
        except pickle.UnpicklingError as exc:
            raise ValueError("Unpickled data contains disallowed objects.") from exc