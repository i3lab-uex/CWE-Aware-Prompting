import json

# List of allowed serialization methods – only safe ones are included.
ALLOWED_METHODS = {"json"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into its corresponding Python object using
    only whitelisted serialization methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data as a byte stream.
    method_of_serialization : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not in ALLOWED_METHODS or
        if deserialization fails.
    """
    # Normalise method name (case‑insensitive)
    method = method_of_serialization.strip().lower()

    if method not in ALLOWED_METHODS:
        raise ValueError(
            f"Deserialization method '{method_of_serialization}' is not allowed."
        )

    if method == "json":
        try:
            # JSON expects a text string; decode from UTF‑8.
            return json.loads(data_bytes_stream.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled deserialization method: {method}")