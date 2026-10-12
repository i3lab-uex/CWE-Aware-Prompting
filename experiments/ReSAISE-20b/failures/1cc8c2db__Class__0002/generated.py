import json
import yaml

# List of trusted serialization formats
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str):
    """
    Deserialize `data` according to the specified `signature`.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    signature : str
        The format of the serialized data (e.g. 'json', 'yaml').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided `signature` is not in the list of trusted signatures.
    """
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Decode bytes to string for json/yaml parsing
    text = data.decode("utf-8")

    if signature == "json":
        return json.loads(text)
    elif signature == "yaml":
        # Use safe_load to avoid arbitrary code execution
        return yaml.safe_load(text)

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {signature}")