import json
import csv
import io

# Optional: YAML support if the dependency is available.
try:
    import yaml  # type: ignore
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False

# List of methods that are considered safe for deserialization.
SAFE_METHODS = {"json", "csv"}
if _YAML_AVAILABLE:
    SAFE_METHODS.add("yaml")


def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into a Python object using the specified method.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data as a byte stream.
    method_of_serialization : str
        Identifier of the serialization format. Allowed values are:
            - 'json'
            - 'csv'
            - 'yaml' (only if PyYAML is installed)

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested method is not in SAFE_METHODS.
    """
    method = method_of_serialization.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed or not recognized.")

    # Decode bytes safely. UTF-8 is the common default; adjust if needed.
    try:
        text = data_bytes_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream is not valid UTF-8.") from exc

    if method == "json":
        # json.loads is safe for JSON data.
        return json.loads(text)

    if method == "csv":
        # CSV is read into a list of dictionaries (header as keys).
        f = io.StringIO(text)
        reader = csv.DictReader(f)
        return [row for row in reader]

    if method == "yaml":
        # Safe loading with PyYAML's safe_load.
        return yaml.safe_load(text)

    # This point should never be reached because of the earlier check.
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")