import json
import yaml

# List of trusted serialization formats
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str):
    """
    Deserialize data from an untrusted source using only trusted formats.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    signature : str
        The format of the serialized data (e.g., 'json', 'yaml').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the signature is not in the list of trusted formats.
    """
    if signature.lower() not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Decode bytes to string if necessary
    if isinstance(data, bytes):
        data_str = data.decode("utf-8")
    else:
        data_str = str(data)

    if signature.lower() == "json":
        return json.loads(data_str)
    elif signature.lower() == "yaml":
        # Use safe_load to avoid arbitrary code execution
        return yaml.safe_load(data_str)
    else:
        # This branch is unreachable due to the earlier check,
        # but kept for completeness.
        raise ValueError(f"Unsupported format: {signature}")