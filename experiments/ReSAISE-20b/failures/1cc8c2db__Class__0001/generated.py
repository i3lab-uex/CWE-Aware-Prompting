import json
import yaml

# List of trusted signatures.  Only these formats are allowed.
TRUSTED_SIGNATURES = {"json", "yaml"}


def deserialize_data(data: bytes, signature: str):
    """
    Deserialize `data` according to the provided `signature`.

    Parameters
    ----------
    data : bytes
        The serialized byte string to deserialize.
    signature : str
        One of the supported serialization formats (e.g. 'json', 'yaml').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the supplied signature is not in the list of trusted signatures.
    """
    # Normalise the signature to lower case for comparison
    sig = signature.lower()

    if sig not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported serialization format: {signature!r}")

    # Decode bytes to string for text-based formats
    try:
        text = data.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Data is not valid UTF‑8") from exc

    if sig == "json":
        return json.loads(text)

    # At this point we know it is 'yaml'
    return yaml.safe_load(text)