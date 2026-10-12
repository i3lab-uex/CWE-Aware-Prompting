import json
import configparser
import pickle
from io import BytesIO
from typing import Any


class SafeUnpickler(pickle.Unpickler):
    """
    A restricted unpickler that only allows a small set of safe built‑in types.
    """
    # Allowed builtins
    _allowed = {
        'int', 'float', 'complex', 'str', 'bytes',
        'list', 'tuple', 'dict', 'set', 'frozenset',
    }

    def find_class(self, module: str, name: str):
        # Only allow builtins
        if module == "builtins" and name in self._allowed:
            return getattr(pickle, name, None) or __builtins__[name]
        raise pickle.UnpicklingError(
            f"Disallowed pickle object: {module}.{name}"
        )


def convert_serialized_data(raw_bytes: bytes, format_hint: str) -> Any:
    """
    Deserialize *raw_bytes* according to *format_hint*.

    Supported formats (safe only):
        - 'json' : JSON data
        - 'ini'  : INI configuration file (converted to nested dict)
        - 'pickle': Python pickle data, but only for a restricted set of safe types

    Raises:
        ValueError: if the format is unsupported or unsafe.
    """
    fmt = format_hint.lower()
    if fmt == "json":
        try:
            return json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a text stream; decode as UTF‑8.
            parser.read_file(BytesIO(raw_bytes))
        except Exception as exc:
            raise ValueError(f"Invalid INI data: {exc}") from exc

        # Convert to a plain dict of dicts
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    if fmt == "pickle":
        try:
            return SafeUnpickler(BytesIO(raw_bytes)).load()
        except Exception as exc:
            raise ValueError(f"Unsafe or invalid pickle data: {exc}") from exc

    raise ValueError(f"Unsupported format hint: {format_hint!r}")