import json
import hmac
import hashlib

# Example global dictionary of device IDs to their shared secret keys (not signatures)
TRUSTED_DEVICE_SIGNATURES = {
    # device_id: shared_secret_key
    "device_001": b"supersecretkey1",
    "device_002": b"anotherverysecret2",
    # Add more devices as needed
}

def _serialize_packet(packet: dict) -> bytes:
    """
    Serialize the data packet into a deterministic byte string.
    Uses JSON with sorted keys to ensure consistent ordering.
    """
    return json.dumps(packet, sort_keys=True, separators=(",", ":")).encode("utf-8")

def _compute_hmac(secret: bytes, message: bytes) -> str:
    """
    Compute an HMAC-SHA256 signature for the given message.
    Return the hex representation of the digest.
    """
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

def process_packet(device_id: str, packet_signature: str, data_packet: dict) -> dict | None:
    """
    Validate and process a packet from an IoT device.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending device.
    packet_signature : str
        Hex-encoded cryptographic signature provided with the packet.
    data_packet : dict
        Payload of the packet.

    Returns
    -------
    dict | None
        The processed data if signature verification succeeds; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully.
    """
    # Simulate a failure to receive the packet
    if data_packet is None:
        raise ConnectionError(f"Unable to receive packet from device {device_id}")

    # Retrieve the shared secret for the device
    secret = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not secret:
        # Unknown device: treat as signature failure
        return None

    # Compute the expected HMAC of the serialized packet
    message = _serialize_packet(data_packet)
    expected_signature = _compute_hmac(secret, message)

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_signature, packet_signature.lower()):
        return None

    # Signature verified – process the data
    # (For this example we simply return the packet unchanged)
    processed_data = dict(data_packet)  # shallow copy to avoid accidental mutation
    return processed_data