import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real values in production.
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # ...
}

def handle_data_packet(device_id: str, signature: str, data: Dict) -> Optional[Dict]:
    """
    Process a data packet from an IoT device after verifying its cryptographic signature.

    Parameters
    ----------
    device_id : str
        The identification number of the IoT device that sent the data.
    signature : str
        The cryptographic signature accompanying the packet.
    data : dict
        The payload of the packet that needs to be processed.

    Returns
    -------
    dict or None
        The data dictionary if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the data packet is not received properly (e.g., missing payload or wrong type).
    """
    # Validate the incoming packet structure.
    if data is None:
        raise ConnectionError("Data payload is missing.")
    if not isinstance(data, dict):
        raise ConnectionError(f"Expected data to be a dict, got {type(data).__name__}.")

    # Retrieve the trusted signature for this device.
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not trusted_sig:
        # Device is unknown; treat as invalid.
        return None

    # Perform a timing‑attack resistant comparison of signatures.
    if not hmac.compare_digest(signature, trusted_sig):
        return None

    # Signature is valid – return the payload for further processing.
    return data