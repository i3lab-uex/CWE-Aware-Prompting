import json
import configparser
from typing import Any

def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Safely deserialize binary payloads that are known to be in one of the
    supported formats: JSON, INI (via configparser), or a simple key/value
    text format. Any other format is considered unsafe and will raise an exception.

    Parameters
    ----------
    payload_bytes : bytes
        The binary data to deserialize.
    schema_type : str
        One of "json", "ini".  The comparison is case‑insensitive.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.  For JSON this is
        a dict/list/etc.  For INI this is a ConfigParser object.

    Raises
    ------
    ValueError
        If the schema_type is not supported or if deserialization fails.
    """
    # Normalize format name
    fmt = schema_type.strip().lower()

    try:
        if fmt == "json":
            # JSON is safe for basic data types; decode to str first
            text = payload_bytes.decode("utf-8")
            return json.loads(text)

        elif fmt == "ini":
            # INI is parsed into a ConfigParser object; no arbitrary code execution
            config = configparser.ConfigParser()
            # read_string expects a str, not bytes
            text = payload_bytes.decode("utf-8")
            config.read_string(text)
            return config

        else:
            raise ValueError(f"Unsupported or unsafe schema type: {schema_type!r}")

    except (json.JSONDecodeError, configparser.Error) as exc:
        # Wrap underlying parsing errors with a generic ValueError
        raise ValueError(f"Failed to deserialize payload as {schema_type!r}: {exc}") from exc