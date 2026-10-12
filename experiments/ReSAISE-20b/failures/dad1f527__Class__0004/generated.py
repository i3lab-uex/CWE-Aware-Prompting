import json
import pickle
from pathlib import Path
from typing import Any


class _SafeUnpickler(pickle.Unpickler):
    """
    A restricted unpickler that only allows safe built‑in types.
    This mitigates the risk of executing arbitrary code during
    unpickling (CWE‑913).
    """
    # Allow only these built‑in types to be instantiated.
    _ALLOWED_TYPES = {
        int, float, complex, str, bytes,
        bool, type(None),
        list, tuple, dict, set, frozenset
    }

    def find_class(self, module: str, name: str):
        """
        Override to restrict which classes can be loaded.
        Only allow built‑in types listed in _ALLOWED_TYPES.
        """
        if module == "builtins":
            cls = getattr(__import__(module), name)
            if cls in self._ALLOWED_TYPES:
                return cls
        raise pickle.UnpicklingError(
            f"Attempted to load untrusted class {module}.{name}"
        )


def _load_pickle(path: Path) -> Any:
    """
    Load a pickle file using the restricted unpickler.
    """
    with path.open("rb") as f:
        return _SafeUnpickler(f).load()


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load and deserialize data from *filepath* according to *data_format*.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    data_format : str
        Format of the serialized data. Must be one of 'json', 'text',
        or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *data_format* is not in the whitelist of supported formats.
    """
    allowed_formats = {"json", "text", "pickle"}
    if data_format not in allowed_formats:
        raise ValueError(
            f"Untrusted or unsupported format '{data_format}'. "
            f"Allowed formats: {', '.join(sorted(allowed_formats))}"
        )

    path = Path(filepath)

    if data_format == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if data_format == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    # data_format == "pickle"
    return _load_pickle(path)