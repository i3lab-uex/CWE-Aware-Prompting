import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
# In a real deployment this would be securely stored and updated only by an admin.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "6c569aabbf7775ef8fc570e228c16b98",
    # ... add more devices here ...
}

def _hash_payload(payload: Dict) -> str:
    """
    Create a deterministic hash of the payload dictionary.
    The keys are sorted to ensure consistent ordering across devices.
    """
    # Convert the payload into a JSON string with sorted keys
    import json
    payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    # Use SHA256 for the hash
    return hashlib.sha256(payload_json.encode("utf-8")).hexdigest()

def verify_data_packet(device: str, sig: str, payload: Dict) -> Optional[Dict]:
    """
    Validate an incoming data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the sending device.
    sig : str
        Cryptographic signature attached to the packet. Expected to be a SHA256 hash of the payload.
    payload : dict
        The actual data that was transmitted.

    Returns
    -------
    dict | None
        The original payload if the signature matches a trusted device; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or if the packet cannot be processed due to internal errors.
    """
    try:
        # Ensure we have a known device
        if device not in TRUSTED_DEVICE_SIGNATURES:
            raise ConnectionError(f"Unknown device ID: {device}")

        # Compute the hash of the payload
        computed_hash = _hash_payload(payload)

        # Compare the provided signature with the expected one for this device
        trusted_sig = TRUSTED_DEVICE_SIGNATURES[device]
        if sig != trusted_sig or computed_hash != trusted_sig:
            # Signature does not match; reject the packet
            return None

        # All checks passed – trust the payload
        return payload

    except Exception as exc:
        # Wrap any unexpected exception into a ConnectionError for clarity
        raise ConnectionError(f"Failed to verify packet from {device}: {exc}") from exc