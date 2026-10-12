import json
import configparser
import io

# Optional: include yaml if available, but keep it safe by using safe_load
try:
    import yaml  # type: ignore
except ImportError:   # pragma: no cover
    yaml = None


def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Deserialize binary data into a Python object using only approved formats.

    Parameters
    ----------
    data_input : bytes
        Serialized data received in binary format.
    format_type : str
        The serialization mechanism used: 'json', 'ini', or 'yaml'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in the allowed list or if deserialization fails.
    """
    if not isinstance(data_input, (bytes, bytearray)):
        raise TypeError("data_input must be bytes or bytearray")

    # Decode to string using UTF-8; ignore errors to avoid crashes
    text = data_input.decode("utf-8", errors="ignore")

    fmt = format_type.lower()

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(io.StringIO(text))
        except configparser.Error as exc:
            raise ValueError(f"INI deserialization error: {exc}") from exc
        # Convert to a nested dictionary for easier use
        return {section: dict(parser[section]) for section in parser.sections()}

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("PyYAML is not installed; cannot deserialize YAML")
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ValueError(f"YAML deserialization error: {exc}") from exc

    # If we reach here, the format is not supported
    raise ValueError(f"Unsupported or disallowed format: {format_type}")