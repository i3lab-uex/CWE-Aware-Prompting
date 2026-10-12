import json
import configparser
from typing import Any, Union


def safely_deserialize_data(
    serialized_bytes: bytes,
    method_format: str
) -> Any:
    """
    Safely deserialize binary data using a whitelisted format.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary payload received from an external source.
    method_format : str
        The serialization format used ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist or deserialization fails.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json", "ini"}

    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: {method_format}")

    # Decode bytes to string (UTF-8) for text-based formats
    try:
        decoded = serialized_bytes.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to decode bytes; data may be corrupted") from exc

    if fmt == "json":
        try:
            return json.loads(decoded)
        except Exception as exc:  # pragma: no cover
            raise ValueError("JSON deserialization error") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            parser.read_string(decoded)
        except Exception as exc:  # pragma: no cover
            raise ValueError("INI deserialization error") from exc

        # Convert the ConfigParser object to a nested dictionary
        result: dict[str, dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result