import json
import yaml

# List of trusted serialization formats.
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str):
    """
    Safely deserializes `data` according to the given `signature`.

    Parameters
    ----------
    data : bytes
        The serialized byte sequence to deserialize.
    signature : str
        The format of the serialization (e.g., 'json', 'yaml').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided signature is not in TRUSTED_SIGNATURES.
    """
    sig = signature.lower()
    if sig not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported serialization format: {signature}")

    # Convert bytes to text using UTF-8 (common encoding for json/yaml)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Data is not valid UTF-8 encoded: {exc}") from exc

    if sig == "json":
        return json.loads(text)

    # yaml is the only other trusted format
    if sig == "yaml":
        return yaml.safe_load(text)