import json
from typing import Any

# Optional: If you need YAML support, uncomment the following line and install PyYAML
# import yaml

# Trusted formats for deserialization
_TRUSTED_SIGNATURES = {"json"}  # Add "yaml" if you enable YAML support

def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize data from an untrusted source only if the format is trusted.

    Parameters
    ----------
    data : bytes
        The serialized payload.
    signature : str
        The format of the serialization (e.g. 'json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided signature is not in the list of trusted formats.
    """
    # Ensure we only process trusted signatures
    if signature not in _TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported or untrusted format: {signature}")

    # Decode bytes to string using UTF-8
    text = data.decode("utf-8")

    if signature == "json":
        return json.loads(text)

    # If you enable YAML support, uncomment the block below
    # if signature == "yaml":
    #     return yaml.safe_load(text)

    # Should never reach here due to the trusted set check
    raise ValueError(f"Unhandled format: {signature}")