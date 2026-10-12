import json
from configparser import ConfigParser
from typing import Any, Dict


# A whitelist of serialization formats that are considered safe.
ALLOWED_FORMATS = {"json", "ini"}


def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data safely based on the specified format.

    Parameters
    ----------
    byte_data : bytes
        The serialized data received in binary form.
    serialization_format : str
        The name of the serialization format used ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object. For `json` this is the usual JSON
        decoded structure; for `ini` it is a nested dictionary mirroring the
        section/key/value layout.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed serialization format: {serialization_format}")

    try:
        if fmt == "json":
            # Decode bytes to string, then load JSON. This prevents executing code.
            text = byte_data.decode("utf-8")
            return json.loads(text)

        if fmt == "ini":
            # Use ConfigParser to parse INI data into a dictionary.
            config = ConfigParser()
            config.read_string(byte_data.decode("utf-8"))
            # Convert to a nested dict: {section: {key: value}}
            result: Dict[str, Dict[str, str]] = {}
            for section in config.sections():
                result[section] = dict(config.items(section))
            return result

    except Exception as exc:
        # Wrap any exception in a ValueError to avoid leaking implementation details.
        raise ValueError(f"Failed to deserialize data: {exc}") from exc