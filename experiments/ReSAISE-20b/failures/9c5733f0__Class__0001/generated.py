import hmac
import hashlib
from typing import Dict, Any

# Global dictionary mapping device IDs to their shared secret keys (hex strings)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in real usage these would be securely stored and managed
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}


def _receive_packet(id_device: str) -> Dict[str, Any]:
    """
    Simulated low‑level packet reception. In a real system this would
    involve network I/O, TLS sockets, or message queue consumers.

    Raises:
        ConnectionError: If the packet cannot be retrieved.
    """
    # Placeholder implementation – replace with real I/O logic
    if id_device not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device '{id_device}'")
    # Simulate successful reception
    return {"dummy": "data"}


def _compute_hmac(secret: str, data_bytes: bytes) -> str:
    """
    Compute an HMAC‑SHA256 signature for the given data using the supplied
    secret key. The result is returned as a hexadecimal string.
    """
    key_bytes = bytes.fromhex(secret)
    mac = hmac.new(key_bytes, data_bytes, hashlib.sha256)
    return mac.hexdigest()


def process_packet_data(id_device: str, packet_signature: str, packet_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Validate the cryptographic signature of an incoming packet from an IoT device
    and return the packet data if it is authentic.

    Parameters:
        id_device (str): Unique identifier of the sending device.
        packet_signature (str): Hexadecimal HMAC‑SHA256 signature supplied with the packet.
        packet_data (dict): Payload of the packet.

    Returns:
        dict: The original packet data if the signature is valid.
        None: If the signature does not match.

    Raises:
        ConnectionError: If packet reception fails (e.g., network issue).
    """
    # 1. Ensure we can receive data from the device
    try:
        _receive_packet(id_device)
    except ConnectionError as e:
        # Propagate connection errors to the caller
        raise

    # 2. Retrieve the shared secret for this device
    secret = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if not secret:
        # Device is unknown – treat as invalid
        return None

    # 3. Compute expected signature in a constant‑time manner
    try:
        data_bytes = bytes(str(packet_data), encoding="utf-8")
    except Exception as exc:
        # If data cannot be serialized, treat as invalid
        return None

    expected_signature = _compute_hmac(secret, data_bytes)

    # 4. Compare signatures using constant‑time comparison
    if hmac.compare_digest(expected_signature, packet_signature.lower()):
        return packet_data
    else:
        # Signature mismatch – do not trust the data
        return None