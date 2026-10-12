import hmac
import hashlib

# Global mapping of device IDs to their expected cryptographic signatures.
# In a real system this would be securely stored and protected.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "6cb75f652a9b52798eb6cf2201057c73",
    # Add more device signatures as needed.
}

def _compute_signature(dev_id: str, packet_content: dict) -> str:
    """
    Compute the HMAC-SHA256 signature for a packet using a device-specific secret.
    For demonstration purposes, the secret is derived from the trusted signature itself.
    In production, a dedicated secret key per device should be used.
    """
    secret = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if not secret:
        raise ValueError("Unknown device ID")

    # Convert packet content to a canonical string representation.
    # Sorting keys ensures consistent ordering for signature calculation.
    payload = "".join(f"{k}={v}" for k, v in sorted(packet_content.items()))
    digest = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return digest

def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: dict):
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the sending IoT device.
    crypto_sign : str
        Cryptographic signature provided with the packet.
    packet_content : dict
        The actual data payload of the packet.

    Returns
    -------
    dict or None
        Returns the packet content if authentication succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet content is missing or cannot be retrieved.
    ValueError
        If the device ID is unknown (internal error).
    """
    # Simulate a potential data-reception issue.
    if packet_content is None:
        raise ConnectionError("Failed to receive data from IoT device")

    # Validate that the device is known.
    if dev_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ValueError(f"Unrecognized device ID: {dev_id}")

    # Compute the expected signature.
    try:
        expected_sign = _compute_signature(dev_id, packet_content)
    except Exception as e:
        # Unexpected error during signature computation
        raise ValueError(f"Signature computation failed: {e}")

    # Use a timing‑safe comparison to prevent side‑channel attacks.
    if not hmac.compare_digest(expected_sign, crypto_sign):
        return None  # Signature mismatch

    # At this point the packet is authenticated; return the payload.
    return packet_content