import hmac
import hashlib

# Global mapping of device IDs to their trusted HMAC secret keys (hex encoded)
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "device_002": "0f1e2d3c4b5a69788776655443322110",
    # Add more device keys as needed
}

def _verify_signature(device_id: str, signature: str, data: dict) -> bool:
    """
    Verify the HMAC-SHA256 signature of the payload.
    The signature is expected to be a hex string.
    """
    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        return False

    # Convert the secret key from hex to bytes
    secret_key = bytes.fromhex(TRUSTED_DEVICE_SIGNATURES[device_id])

    # Serialize the data to a canonical form (sorted keys) for deterministic hashing
    serialized = ",".join(f"{k}={v}" for k, v in sorted(data.items()))
    computed = hmac.new(secret_key, serialized.encode("utf-8"), hashlib.sha256).hexdigest()

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(computed, signature)

def handle_data_packet(device_id: str, signature: str, data: dict):
    """
    Process a data packet from an IoT device after verifying its cryptographic signature.

    Args:
        device_id (str): Identification number of the sending IoT device.
        signature (str): Cryptographic HMAC-SHA256 signature accompanying the packet (hex).
        data (dict): Payload of the packet.

    Returns:
        dict | None: The payload dictionary if signature is valid, otherwise None.

    Raises:
        ConnectionError: If the packet data is missing or malformed.
    """
    # Basic sanity checks for packet reception
    if not isinstance(data, dict) or data is None:
        raise ConnectionError("Data packet not received properly")

    # Verify the signature
    if _verify_signature(device_id, signature, data):
        return data

    # Signature invalid
    return None