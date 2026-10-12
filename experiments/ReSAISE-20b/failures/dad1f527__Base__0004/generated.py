import json
import pickle
from pathlib import Path
from typing import Any


class RestrictedUnpickler(pickle.Unpickler):
    """
    A restricted unpickler that only allows a safe set of classes.
    This is a minimal example; in production you should customize the
    whitelist to your specific needs.
    """
    SAFE_NAMES = {
        'builtins.str',
        'builtins.int',
        'builtins.float',
        'builtins.bool',
        'builtins.list',
        'builtins.tuple',
        'builtins.dict',
        'builtins.set',
    }

    def find_class(self, module: str, name: str):
        full_name = f"{module}.{name}"
        if full_name not in self.SAFE_NAMES:
            raise pickle.UnpicklingError(f"Attempting to unpickle disallowed class: {full_name}")
        return super().find_class(module, name)


def load_serialized_data(filepath: str | Path, data_format: str) -> Any:
    """
    Load serialized data from a file using only whitelisted formats.

    Parameters
    ----------
    filepath : str | Path
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
        If the format is not in the whitelist.
    FileNotFoundError, OSError
        For file I/O errors.
    """
    allowed_formats = {'json', 'text', 'pickle'}
    fmt = data_format.lower()
    if fmt not in allowed_formats:
        raise ValueError(f"Untrusted or unsupported data format: {data_format}")

    path = Path(filepath)
    if fmt == 'json':
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)

    if fmt == 'text':
        with path.open('r', encoding='utf-8') as f:
            return f.read()

    # fmt == 'pickle'
    with path.open('rb') as f:
        return RestrictedUnpickler(f).load()


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     obj = load_serialized_data("data.json", "json")
#     print(obj)