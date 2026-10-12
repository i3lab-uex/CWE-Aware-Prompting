import json
import pickle
from pathlib import Path
from typing import Any


class RestrictedUnpickler(pickle.Unpickler):
    """
    A minimal unpickler that only allows safe built‑in types.
    It forbids loading arbitrary classes or modules which can lead to
    code execution (CWE‑502).
    """
    # Whitelisted safe types from the builtins module
    _SAFE_BUILTINS = {
        'builtins': {'list', 'dict', 'str', 'int', 'float', 'bool', 'NoneType'},
    }

    def find_class(self, module: str, name: str) -> Any:
        """Override to restrict loaded classes."""
        if module in self._SAFE_BUILTINS and name in self._SAFE_BUILTINS[module]:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(
            f"Attempted to load unsafe class {module}.{name}"
        )


def interpret_serialized_content(src_file: str, content_type: str) -> Any:
    """
    Deserialize data from a file in a safe manner.

    Parameters
    ----------
    src_file : str
        Path to the file containing serialized data.
    content_type : str
        The format of the serialized data. Must be one of:
        'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the content_type is unsupported or if deserialization fails.
    """
    allowed_types = {"json", "text", "pickle"}
    if content_type not in allowed_types:
        raise ValueError(f"Unsupported content type: {content_type}")

    path = Path(src_file)
    if not path.is_file():
        raise ValueError(f"File does not exist: {src_file}")

    try:
        if content_type == "json":
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)

        if content_type == "text":
            with path.open("r", encoding="utf-8") as f:
                return f.read()

        # content_type == "pickle"
        with path.open("rb") as f:
            return RestrictedUnpickler(f).load()

    except (json.JSONDecodeError, pickle.UnpicklingError, OSError) as exc:
        raise ValueError(f"Failed to deserialize {src_file}: {exc}") from exc