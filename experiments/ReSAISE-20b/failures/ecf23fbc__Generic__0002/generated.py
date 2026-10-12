import json
import pickle
from pathlib import Path

# --------------------------------------------------------------------------- #
# Restricted unpickler – only allows basic built‑in types
# --------------------------------------------------------------------------- #
class _RestrictedUnpickler(pickle.Unpickler):
    """A pickle.Unpickler that only permits safe built‑in types."""
    # Whitelisted modules and classes
    _allowed_builtins = {
        'builtins': {'list', 'dict', 'set', 'tuple', 'frozenset',
                     'int', 'float', 'bool', 'str', 'bytes', 'NoneType'}
    }

    def find_class(self, module: str, name: str):
        if (module in self._allowed_builtins and
                name in self._allowed_builtins[module]):
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(
            f"Disallowed class: {module}.{name}"
        )

def restricted_loads(data: bytes):
    """Load pickle data using the restricted unpickler."""
    return _RestrictedUnpickler(io.BytesIO(data)).load()


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def interpret_serialized_content(src_file: str, content_type: str):
    """
    Deserialize data from a file in a safe manner.

    Parameters
    ----------
    src_file : str
        Path to the file containing serialized data.
    content_type : str
        Serialization format. Must be one of:
            'json'   – JSON text.
            'text'   – Plain UTF‑8 string.
            'pickle' – Pickle data (restricted to safe types).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the content_type is unsupported or unsafe.
    """
    # Normalise the format string
    fmt = content_type.lower()
    if fmt not in {'json', 'text', 'pickle'}:
        raise ValueError(f"Unsupported content type: {content_type}")

    path = Path(src_file)

    if fmt == 'json':
        with path.open('r', encoding='utf-8') as fp:
            return json.load(fp)

    if fmt == 'text':
        with path.open('r', encoding='utf-8') as fp:
            return fp.read()

    # fmt == 'pickle'
    with path.open('rb') as fp:
        data = fp.read()
    try:
        return restricted_loads(data)
    except pickle.UnpicklingError as exc:
        raise ValueError("Unsafe pickle data") from exc


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     obj = interpret_serialized_content('data.json', 'json')
#     print(obj)