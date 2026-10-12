import json
from typing import Any

# Import yaml only if available and safe.  If not installed, raise an informative error.
try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# Define a whitelist of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "yaml"}


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Deserialize binary data using only a pre-approved format.

    Parameters
    ----------
    serialized_bytes : bytes
        Binary data to be deserialized.
    method_format : str
        The serialization format used (e.g., 'json', 'yaml').

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist or if the data cannot be parsed.
    ImportError
        If a required library for the format is missing (e.g., yaml).
    """
    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Format '{method_format}' is not allowed. Allowed formats: {sorted(SAFE_FORMATS)}")

    # Convert bytes to text using UTF-8.  If decoding fails, raise a ValueError.
    try:
        text = serialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Failed to decode bytes: {exc}") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    if fmt == "yaml":
        if yaml is None:
            raise ImportError("PyYAML is required for YAML deserialization but is not installed.")
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:  # pragma: no cover
            raise ValueError(f"YAML deserialization error: {exc}") from exc

    # This point should never be reached due to the whitelist check.
    raise ValueError(f"Unhandled format: {method_format}")