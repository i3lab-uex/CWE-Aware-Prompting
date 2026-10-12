import json
import yaml

# Trusted serialization formats
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str):
    """
    Deserialize `data` according to the provided `signature`.

    Parameters
    ----------
    data : bytes
        The serialized data.
    signature : str
        The format of the serialized data (e.g. 'json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the signature is not in the list of trusted formats.
    """
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Decode bytes to string for JSON/YAML parsing
    text = data.decode("utf-8")

    if signature == "json":
        return json.loads(text)
    elif signature == "yaml":
        return yaml.safe_load(text)

    # The following line is unreachable because of the earlier check,
    # but kept for clarity.
    raise ValueError(f"Unsupported format: {signature}")