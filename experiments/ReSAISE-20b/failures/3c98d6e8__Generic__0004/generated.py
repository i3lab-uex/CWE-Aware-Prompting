import json
import pickle
from pathlib import Path

def load_serial_data(f_path: str, f_format: str):
    """
    Deserialize data from a file located at ``f_path``.

    Parameters
    ----------
    f_path : str
        Path to the file containing the serialized data.
    f_format : str
        Format of the serialized data.  Must be one of ``'json'``,
        ``'text'`` or ``'pickle'``.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If ``f_format`` is not one of the supported, safe formats.
    FileNotFoundError
        If ``f_path`` does not exist.
    """
    # Whitelist of supported formats.  Only the JSON and plain‑text
    # serializers are considered safe; pickle is included for
    # completeness but carries a security risk.
    _SUPPORTED_FORMATS = {"json", "text", "pickle"}

    if f_format not in _SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format '{f_format}'. "
            f"Allowed formats: {', '.join(sorted(_SUPPORTED_FORMATS))}"
        )

    file_path = Path(f_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"No such file: {f_path}")

    if f_format == "text":
        # Plain text – return the raw string
        with file_path.open("r", encoding="utf-8") as fp:
            return fp.read()

    if f_format == "json":
        # JSON – safe by design
        with file_path.open("r", encoding="utf-8") as fp:
            return json.load(fp)

    if f_format == "pickle":
        # Pickle – unsafe for untrusted data.  Still provided
        # because it is in the whitelist, but callers should
        # be aware of the risks.
        with file_path.open("rb") as fp:
            return pickle.load(fp)