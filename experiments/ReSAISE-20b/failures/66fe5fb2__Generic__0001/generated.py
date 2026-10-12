import json
import configparser
from typing import Any, Dict


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Deserialize binary data that was serialized using a known, safe format.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw binary data received from an external source.
    method_format : str
        One of the supported serialization formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the specified format is not supported or if deserialization fails.
    """
    # Define the set of formats that are considered safe
    SAFE_FORMATS = {"json", "ini"}

    if method_format not in SAFE_FORMATS:
        raise ValueError(
            f"Deserialization format '{method_format}' is not supported or allowed."
        )

    try:
        if method_format == "json":
            # JSON expects a string; decode using UTF-8
            return json.loads(serialized_bytes.decode("utf-8"))

        if method_format == "ini":
            # configparser requires a file-like object; use StringIO
            cfg = configparser.ConfigParser()
            cfg.read_string(serialized_bytes.decode("utf-8"))
            # Convert to a plain dictionary for easier consumption
            return {section: dict(cfg[section]) for section in cfg.sections()}

    except Exception as exc:
        # Wrap any underlying exception into a ValueError with context
        raise ValueError(f"Failed to deserialize data using format '{method_format}': {exc}") from exc