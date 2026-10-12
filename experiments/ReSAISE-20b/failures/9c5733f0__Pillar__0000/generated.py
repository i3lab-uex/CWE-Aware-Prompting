import hashlib
import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected HMAC signatures.
# In a real deployment this would be stored securely, e.g. in a vault or
# hardware security module (HSM). For illustration we use an in‑memory dict.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id : expected_hmac_hex)
    "device_001": "5e884898da28047151d0e56f8dc6292773603d0d6aabbddf9c2b7e4b1ed5cf3a",
    "device_002": "6f8db599de986fab7a21625b7916589c0e4d5c6f2c3b1a7d5e8cf9b0ac2e4b45",
    # Add more devices as needed
}


def _compute_hmac(device_id: str, packet_data: Dict) -> str:
    """
    Compute a SHA‑256 HMAC over the JSON representation of packet_data
    concatenated with the device_id.  The resulting digest is returned as a
    hexadecimal string.
    """
    # Serialize packet_data deterministically to avoid ordering issues
    import json
    payload = json.dumps(packet_data, sort_keys=True).encode("utf-8")
    # Use the device_id as the key for HMAC
    key = device_id.encode("utf-8")
    digest = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return digest


def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of a packet from an IoT device and
    return the packet data if the signature is valid.

    Parameters
    ----------
    id_device : str
        Unique identifier of the sending device.
    packet_signature : str
        Hexadecimal HMAC signature supplied with the packet.
    packet_data : dict or None
        The actual payload of the packet.  If ``None`` a
        :class:`ConnectionError` is raised to indicate a failure in
        receiving data.

    Returns
    -------
    dict or None
        The packet payload if the signature matches; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If packet_data is None, indicating a communication failure.
    """
    # Simulate a connection error if no data was received
    if packet_data is None:
        raise ConnectionError(f"No data received from device '{id_device}'")

    # Ensure the device is known
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if not expected_signature:
        # Unknown device – treat as untrusted
        return None

    # Compute the expected HMAC over the received data
    computed_signature = _compute_hmac(id_device, packet_data)

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_signature, packet_signature):
        # Signature mismatch – data is untrusted
        return None

    # All checks passed; return the trusted payload
    return packet_data