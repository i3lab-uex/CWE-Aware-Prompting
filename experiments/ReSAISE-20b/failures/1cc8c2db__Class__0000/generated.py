import json
import yaml

# Trusted formats that are allowed to be deserialized.
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str):
    """
    Deserialize data from an untrusted source into a Python object.

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
        If the provided signature is not in the list of trusted signatures.
    """
    if signature.lower() not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Convert bytes to string if necessary
    if isinstance(data, bytes):
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF-8 encoded text.") from exc
    else:
        raise TypeError("data must be of type bytes")

    if signature.lower() == "json":
        return json.loads(text)
    elif signature.lower() == "yaml":
        # Use safe_load to avoid executing arbitrary tags
        return yaml.safe_load(text)