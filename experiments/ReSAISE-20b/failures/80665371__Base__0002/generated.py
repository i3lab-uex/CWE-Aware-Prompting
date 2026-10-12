import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures (hex strings)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with actual device signatures
    "device_001": "a1b2c3d4e5f6... (hex signature)",
    "device_002": "deadbeef1234... (hex signature)",
}


def process_data_packet(dev_id: str, sign: str, payload: Dict) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device that sent the packet.
    sign : str
        Cryptographic signature attached to the packet (hex encoded).
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is verified successfully;
        otherwise, None.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or there are issues receiving a data packet.
    """
    # Ensure we have a trusted signature for this device
    try:
        expected_sig = TRUSTED_DEVICE_SIGNATURES[dev_id]
    except KeyError as exc:
        raise ConnectionError(f"Unknown device ID: {dev_id}") from exc

    # The signature is expected to be a hex string; validate its format
    if not isinstance(sign, str) or len(sign) % 2 != 0:
        # Malformed signature string
        return None

    try:
        received_sig_bytes = bytes.fromhex(sign)
    except ValueError:
        # Invalid hex encoding
        return None

    try:
        expected_sig_bytes = bytes.fromhex(expected_sig)
    except ValueError:
        # Internal configuration error
        raise ConnectionError("Invalid trusted signature format") from None

    # Compute the expected HMAC of the payload using a secure hash algorithm
    # Note: In real-world usage, the secret key should be kept confidential.
    # Here we assume that `expected_sig` is actually a precomputed HMAC value
    # and not the secret key itself. If the signature is generated using a
    # shared secret, replace this block with appropriate key handling.
    payload_bytes = str(payload).encode("utf-8")
    computed_sig = hmac.new(
        key=b"shared_secret_key",  # Replace with the actual secret
        msg=payload_bytes,
        digestmod=hashlib.sha256,
    ).digest()

    # Use constant-time comparison to prevent timing attacks
    if hmac.compare_digest(computed_sig, received_sig_bytes):
        return payload

    # Signature verification failed
    return None