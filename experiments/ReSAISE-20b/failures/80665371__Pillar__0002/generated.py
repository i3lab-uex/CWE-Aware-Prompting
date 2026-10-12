import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (should be populated with real values in production)
    "device-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device-002": "e99a18c428cb38d5f260853678922e03",
    # ... add more device signatures as needed
}

def process_data_packet(dev_id: str, sign: str, payload: Dict) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an incoming IoT data packet and
    return the payload if verification succeeds.

    Args:
        dev_id: Unique identifier of the sending IoT device.
        sign: Cryptographic signature attached to the packet (hex string).
        payload: The actual data dictionary received.

    Returns:
        The payload dictionary if the signature matches the trusted one,
        otherwise None.

    Raises:
        ConnectionError: If there is an issue retrieving the trusted signature
                         for the device (e.g., unknown device ID).
    """
    # Ensure that we have a trusted signature for this device
    try:
        expected_sign = TRUSTED_DEVICE_SIGNATURES[dev_id]
    except KeyError as exc:
        raise ConnectionError(f"Unknown device ID: {dev_id}") from exc

    # Use constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(sign, expected_sign):
        return None

    # Signature verified; safely return the payload
    return payload