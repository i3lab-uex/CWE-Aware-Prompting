import json
from typing import Any

# Optional: If you have PyYAML installed, uncomment the following line
# from yaml import safe_load as yaml_safe_load

# Trusted formats list
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Safely deserializes data from an untrusted source.

    Parameters
    ----------
    data : bytes
        The serialized payload.
    signature : str
        The format of the serialization ('json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided signature is not in TRUSTED_SIGNATURES.
    """
    sig = signature.lower()
    if sig not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Decode bytes to string for JSON/YAML parsing
    text = data.decode("utf-8")

    if sig == "json":
        return json.loads(text)

    # YAML support (requires PyYAML)
    if sig == "yaml":
        try:
            from yaml import safe_load as yaml_safe_load
        except ImportError as exc:
            raise RuntimeError(
                "YAML deserialization requested but PyYAML is not installed."
            ) from exc
        return yaml_safe_load(text)

    # The code should never reach here because of the earlier check
    raise ValueError(f"Unhandled signature: {signature}")