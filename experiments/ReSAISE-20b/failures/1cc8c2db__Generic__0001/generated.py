import json
import yaml  # Requires PyYAML (`pip install pyyaml`)

# Trusted serialization formats
_TRUSTED_FORMATS = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str):
    """
    Deserialize data from an untrusted source.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    signature : str
        The format of the serialized data (e.g. 'json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported format is provided.
    """
    if signature not in _TRUSTED_FORMATS:
        raise ValueError(f"Unsupported format: {signature!r}")

    # Convert bytes to string for text-based formats
    if signature in {"json", "yaml"}:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Data is not valid UTF-8 for {signature!r}") from exc

    if signature == "json":
        return json.loads(text)

    if signature == "yaml":
        # yaml.safe_load is used to avoid executing arbitrary tags
        return yaml.safe_load(text)

    # In theory we never reach here because of the earlier check
    raise ValueError(f"Unhandled format: {signature!r}")