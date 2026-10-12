import json
from typing import Any

# Optional: If you want to support YAML safely, uncomment the following lines
# and install PyYAML (`pip install pyyaml`). 
# import yaml

ALLOWED_FORMATS = {
    "json": json.loads,
    # "yaml": yaml.safe_load,  # Safe YAML deserialization
}

def decode_data_stream(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data : bytes
        The serialized byte stream to deserialize.
    data_format : str
        Format of the serialized data. Supported formats are defined in
        `ALLOWED_FORMATS`.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in `ALLOWED_FORMATS` or if deserialization
        fails.
    """
    # Normalise the format string to lowercase and strip whitespace
    fmt = data_format.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    # Decode bytes to string using UTF-8 (common for JSON/YAML)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    # Retrieve the appropriate deserialization function
    deserialize_fn = ALLOWED_FORMATS[fmt]

    try:
        return deserialize_fn(text)
    except Exception as exc:  # pylint: disable=broad-except
        raise ValueError(f"Deserialization failed for format {fmt}") from exc