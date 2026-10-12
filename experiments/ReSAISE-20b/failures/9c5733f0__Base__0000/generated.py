import json
import hmac
import hashlib

# Global dictionary mapping device IDs to the expected HMAC secret key (hex string).
# In a real deployment this would be stored securely (e.g., in a HSM or vault).
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries
    "device-001": "a1b2c3d4e5f6g7h8i9j0",  # secret key in hex
    "device-002": "1234567890abcdef1234",
}

def _compute_hmac(secret_hex: str, data: dict) -> str:
    """
    Compute the HMAC-SHA256 of a JSON-encoded payload using the provided secret key.
    The secret is expected to be a hex string.
    """
    # Ensure deterministic JSON serialization
    json_payload = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    secret_bytes = bytes.fromhex(secret_hex)
    mac = hmac.new(secret_bytes, json_payload, hashlib.sha256)
    return mac.hexdigest()


def process_packet_data(id_device: str, packet_signature: str, packet_data: dict) -> dict | None:
    """
    Validate the cryptographic signature of a data packet from an IoT device
    and return the packet content if the signature is valid.

    Parameters:
        id_device (str): Unique identifier of the device.
        packet_signature (str): Hex-encoded HMAC-SHA256 signature attached to the packet.
        packet_data (dict): The actual data payload of the packet.

    Returns:
        dict: The original packet_data if signature is valid.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the device is unknown or cannot be authenticated.
    """
    # 1. Ensure the device ID is known
    if id_device not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {id_device}")

    # 2. Compute expected signature
    secret_key_hex = TRUSTED_DEVICE_SIGNATURES[id_device]
    try:
        expected_sig = _compute_hmac(secret_key_hex, packet_data)
    except (ValueError, TypeError) as exc:
        # Likely an issue with the secret key format or packet_data
        raise ConnectionError("Failed to compute signature") from exc

    # 3. Constant-time comparison to mitigate timing attacks
    if hmac.compare_digest(expected_sig, packet_signature):
        return packet_data

    # 4. Signature mismatch
    return None