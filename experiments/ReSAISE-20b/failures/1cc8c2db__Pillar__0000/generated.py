import json
from typing import Any

# Import PyYAML safely; if not available, yaml loading will be disabled
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

# Trusted serialization formats
TRUSTED_SIGNATURES = {"json", "yaml"}


def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize `data` according to the provided `signature`.

    Parameters
    ----------
    data : bytes
        The serialized payload.
    signature : str
        Format identifier: 'json' or 'yaml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the signature is not in TRUSTED_SIGNATURES or if yaml support
        is missing when required.
    """
    sig = signature.lower()
    if sig not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Decode bytes to text
    try:
        text = data.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Data must be valid UTF‑8 bytes: {exc}") from exc

    if sig == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if sig == "yaml":
        if yaml is None:
            raise ValueError("PyYAML is not installed; cannot deserialize YAML.")
        try:
            return yaml.safe_load(text)
        except Exception as exc:
            raise ValueError(f"Invalid YAML data: {exc}") from exc