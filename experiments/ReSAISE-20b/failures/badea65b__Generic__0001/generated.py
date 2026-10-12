import json
import pickle
from pathlib import Path
from typing import Any, Dict


# --------------------------------------------------------------------------- #
#  Restricted unpickler – only allows built‑in types and basic containers
# --------------------------------------------------------------------------- #
class _RestrictedUnpickler(pickle.Unpickler):
    """
    A pickle Unpickler that only allows loading of safe built‑in types.
    It blocks any attempt to instantiate custom classes or modules,
    which prevents arbitrary code execution.
    """
    # Allowed built‑in types that are considered safe
    _allowed_builtins = {
        'list', 'tuple', 'dict', 'set', 'frozenset',
        'int', 'float', 'bool', 'str', 'bytes',
    }

    def find_class(self, module: str, name: str):
        # Only allow builtins from the whitelist
        if module == 'builtins' and name in self._allowed_builtins:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(
            f"Attempt to load unsafe class {module}.{name}"
        )


def _safe_load_pickle(file_obj) -> Any:
    """
    Load a pickle file using the restricted unpickler.
    """
    return _RestrictedUnpickler(file_obj).load()


# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #
def process_serialfile(input_path: str, format_type: str) -> Any:
    """
    Deserialize data from a file in a secure manner.

    Parameters
    ----------
    input_path : str
        Path to the serialized file.
    format_type : str
        One of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in the whitelist.
    """
    # Whitelist of supported formats
    _WHITELIST = {'json', 'text', 'pickle'}

    fmt = format_type.lower()
    if fmt not in _WHITELIST:
        raise ValueError(
            f"Untrusted or unsupported format '{format_type}'. "
            f"Supported formats: {', '.join(_WHITELIST)}"
        )

    path = Path(input_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {input_path}")

    with path.open('rb') as f:
        if fmt == 'json':
            # JSON can be safely loaded with json.loads
            return json.load(f)
        elif fmt == 'text':
            # Return raw text (decode as UTF-8)
            return f.read().decode('utf-8')
        elif fmt == 'pickle':
            # Use the restricted unpickler
            return _safe_load_pickle(f)


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     obj = process_serialfile("data.json", "json")
#     print(obj)