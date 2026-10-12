import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real values.
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # Add more device signatures as needed.
}


def handle_data_packet(device_id: str, signature: str, data) -> Optional[Dict]:
    """
    Process an IoT data packet after verifying its cryptographic signature.

    Parameters
    ----------
    device_id : str
        Identifier of the IoT device that sent the packet.
    signature : str
        Cryptographic signature accompanying the packet.
    data : dict
        Payload of the packet.

    Returns
    -------
    dict or None
        The payload dictionary if the signature is valid; otherwise, `None`.

    Raises
    ------
    ConnectionError
        If the packet is malformed or missing required fields.
    """
    # Validate input types and presence
    if not isinstance(device_id, str) or not device_id:
        raise ConnectionError("Invalid or missing device ID.")
    if not isinstance(signature, str) or not signature:
        raise ConnectionError("Invalid or missing signature.")
    if data is None:
        raise ConnectionError("Data packet not received properly.")
    if not isinstance(data, dict):
        # Attempt to coerce JSON-like string to dict
        try:
            import json

            data = json.loads(data)
        except Exception:
            raise ConnectionError("Data payload is not a valid dictionary.")

    # Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not trusted_sig:
        # Unknown device; treat as untrusted
        return None

    # Use constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(signature, trusted_sig):
        return None

    # Signature verified; return the data payload
    return data