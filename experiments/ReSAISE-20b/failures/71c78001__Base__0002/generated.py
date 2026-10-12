import hmac
import hashlib
import json

# Global mapping of device IDs to their shared secret keys (hex strings)
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "deadbeefcafebabe1234",
    # Add more device secrets here
}


def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: dict) -> dict | None:
    """
    Authenticate and process an IoT data packet.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet (hex-encoded).
    packet_content : dict
        The actual data payload of the packet.

    Returns
    -------
    dict | None
        The original packet content if signature verification succeeds,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or packet content could not be retrieved.
    """
    # Validate input
    if dev_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {dev_id}")

    if packet_content is None:
        raise ConnectionError("No data received from device")

    # Retrieve the shared secret for this device
    secret_hex = TRUSTED_DEVICE_SIGNATURES[dev_id]
    try:
        secret_bytes = bytes.fromhex(secret_hex)
    except ValueError as exc:
        raise ConnectionError(f"Invalid secret format for device {dev_id}") from exc

    # Serialize the packet content to a canonical JSON string
    try:
        payload = json.dumps(packet_content, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConnectionError("Failed to serialize packet content") from exc

    # Compute the expected HMAC-SHA256 signature
    mac = hmac.new(secret_bytes, payload, hashlib.sha256)
    expected_sig = mac.hexdigest()

    # Compare signatures in constant time
    if not hmac.compare_digest(expected_sig, crypto_sign):
        return None

    # Signature verified; return the original data
    return packet_content