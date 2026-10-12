import hmac
import hashlib

# Global mapping of device IDs to expected cryptographic signatures.
# In a real deployment these would be stored securely (e.g., in a hardware
# security module or a protected key vault) and not hard‑coded.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
    # Add more device signatures as needed.
}

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: dict) -> dict | None:
    """
    Validate and process an IoT data packet.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Cryptographic signature supplied with the packet.
    pkt_data : dict
        Payload of the data packet.

    Returns
    -------
    dict | None
        The processed packet if signature validation succeeds,
        otherwise ``None``.
    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., ``pkt_data`` is None).
    """
    # 1. Ensure the packet was received successfully.
    if pkt_data is None:
        raise ConnectionError(f"Packet from device {device_id} could not be received.")

    # 2. Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Unknown device – reject silently to avoid leaking information.
        return None

    # 3. Verify the signature using a constant‑time comparison to avoid
    # timing attacks (CWE-345: insufficient verification of data authenticity).
    if not hmac.compare_digest(crypt_sig, expected_sig):
        return None

    # 4. At this point the packet is authenticated; perform minimal
    # processing. In a real system you would apply business logic here.
    processed = {
        "device_id": device_id,
        "timestamp": pkt_data.get("timestamp"),
        "payload": pkt_data.get("payload"),
    }
    return processed