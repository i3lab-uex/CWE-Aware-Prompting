import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real device IDs and signatures.
    "device_001": "5f2d1c3b8e6a4f7d9c0b2a1e5f6c3d8a",
    "device_002": "9b7e4d2f1c3a8e6b0d5f1a9c2b4e7d3",
    # ...
}


def verify_iot_signature(
    iot_id: str, crypto_signature: str, packet_info: Dict
) -> Optional[Dict]:
    """
    Verify the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    iot_id : str
        Unique identifier for the IoT device sending the data.
    crypto_signature : str
        The cryptographic signature attached to the data packet.
    packet_info : dict
        The actual content of the packet to be processed.

    Returns
    -------
    dict or None
        The original packet_info if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or there was an issue retrieving the expected signature.
    """
    # Simulate a potential data‑receive error (e.g., timeout, network failure).
    try:
        expected_signature = TRUSTED_DEVICE_SIGNATURES[iot_id]
    except KeyError as exc:
        # Unknown device or missing signature – treat as a communication failure.
        raise ConnectionError(f"Unable to retrieve trusted signature for device {iot_id}") from exc

    # Use constant‑time comparison to avoid timing attacks (CWE-347 mitigation).
    if hmac.compare_digest(expected_signature, crypto_signature):
        return packet_info
    else:
        # Invalid signature – do not trust the data.
        return None