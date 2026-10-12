import hashlib
import hmac

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries; in a real system these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1a2b3c4d5e6f7g8h9i0j",
    # Add more devices as needed.
}


def _compute_signature(packet_data: dict, secret_key: str) -> str:
    """
    Compute a SHA256 HMAC signature for the given packet data using the provided secret key.
    The packet data is serialized in a deterministic order to ensure consistent signatures.
    """
    # Serialize the dictionary into a sorted JSON string for consistency
    import json

    serialized = json.dumps(packet_data, sort_keys=True, separators=(",", ":"))
    # Compute HMAC-SHA256
    mac = hmac.new(secret_key.encode("utf-8"), serialized.encode("utf-8"), hashlib.sha256)
    return mac.hexdigest()


def manage_data_packet(io_device_id: str, crypto_signature: str, packet_data: dict) -> dict | None:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        Unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        Cryptographic signature attached to the packet.
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        Returns the packet data if the signature is verified; otherwise, returns None.

    Raises
    ------
    ConnectionError
        If there are any issues receiving a data packet from the device.
    """
    try:
        # Retrieve the trusted signature for this device
        trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
        if not trusted_sig:
            # Unknown device; treat as a connection issue
            raise ConnectionError(f"Unknown IoT device ID: {io_device_id}")

        # Verify the signature using constant‑time comparison
        if not hmac.compare_digest(crypto_signature, trusted_sig):
            # Signature mismatch: data cannot be trusted
            return None

        # Optional: recompute signature to ensure integrity (if the stored signature is a secret key)
        # For demonstration, we assume the stored value is the expected HMAC of packet_data.
        recomputed_sig = _compute_signature(packet_data, trusted_sig)
        if not hmac.compare_digest(crypto_signature, recomputed_sig):
            # The packet data has been tampered with
            return None

        # Signature verified; return the payload
        return packet_data

    except Exception as exc:
        # Wrap any unexpected exception into a ConnectionError to signal packet reception failure
        raise ConnectionError(f"Failed to process data packet from device {io_device_id}") from exc