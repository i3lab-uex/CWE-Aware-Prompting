import json
import hmac
import hashlib

# Example trusted signatures dictionary.
# In a real system this would be securely stored and managed.
TRUSTED_DEVICE_SIGNATURES = {
    # device_id: shared secret key (bytes)
    "device_001": b"supersecretkey1",
    "device_002": b"anothersecretkey2",
}

def _compute_hmac(secret: bytes, payload: dict) -> str:
    """
    Compute an HMAC-SHA256 over the JSON representation of the payload.
    The JSON is encoded with sorted keys to ensure deterministic output.
    """
    json_payload = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hmac.new(secret, json_payload, hashlib.sha256).hexdigest()


def process_packet(device_id: str, packet_signature: str, data_packet: dict) -> dict | None:
    """
    Validate the cryptographic signature of an IoT data packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Hexadecimal HMAC signature sent with the packet.
    data_packet : dict
        The actual content of the data packet.

    Returns
    -------
    dict | None
        The processed data if signature verification succeeds; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet could not be received (e.g., `data_packet` is None).
    """
    # Simulate a reception failure
    if data_packet is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Retrieve the shared secret for the device
    secret = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not secret:
        # Unknown device: treat as untrusted
        return None

    # Compute the expected signature in a constant‑time manner
    try:
        expected_sig = _compute_hmac(secret, data_packet)
    except Exception as exc:
        # Any error in signature computation is treated as a failure
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE-347)
    if not hmac.compare_digest(expected_sig, packet_signature):
        return None

    # At this point the signature is valid; process the data
    # (placeholder for actual processing logic)
    processed_data = dict(data_packet)  # copy to avoid mutating input
    processed_data["validated"] = True
    return processed_data