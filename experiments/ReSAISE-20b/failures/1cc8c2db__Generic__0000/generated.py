import json

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# List of signatures that are considered safe and trusted.
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str):
    """
    Deserialize `data` according to the provided `signature`.

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
        If the provided signature is not in the list of trusted signatures,
        or if a required module for that signature is missing.
    """
    sig = signature.lower()

    if sig not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature!r}")

    # Decode bytes to string for text-based formats
    try:
        decoded = data.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Data must be UTF-8 encoded text") from exc

    if sig == "json":
        return json.loads(decoded)

    if sig == "yaml":
        if yaml is None:  # pragma: no cover
            raise ValueError("PyYAML is not installed")
        return yaml.safe_load(decoded)

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled signature: {signature!r}")