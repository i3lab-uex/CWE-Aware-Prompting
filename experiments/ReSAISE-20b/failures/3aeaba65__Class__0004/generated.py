import json
import hmac
import hashlib
from typing import Dict, Any

# Example global dictionary mapping device IDs to their shared secrets.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # device_id : shared_secret (hex string)
    "device-001": "a1b2c3d4e5f6",
    "device-002": "deadbeef12345678",
    # Add more devices as needed
}

def verify_iot_signature(iot_id: str, crypto_signature: str,
                         packet_info: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Verify the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    iot_id : str
        Unique identifier of the IoT device.
    crypto_signature : str
        Hex-encoded signature received with the packet.
    packet_info : dict
        The payload of the packet.

    Returns
    -------
    dict | None
        The original packet_info if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or a communication error occurs.
    """
    # 1. Ensure the device is known
    if iot_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {iot_id}")

    # 2. Retrieve the shared secret for HMAC computation
    secret_hex = TRUSTED_DEVICE_SIGNATURES[iot_id]
    try:
        secret_bytes = bytes.fromhex(secret_hex)
    except ValueError as exc:
        raise ConnectionError(f"Invalid secret format for device {iot_id}") from exc

    # 3. Serialize the packet payload in a deterministic way
    try:
        serialized = json.dumps(packet_info, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        # Malformed packet; treat as communication error
        raise ConnectionError("Failed to serialize packet_info") from exc

    # 4. Compute HMAC-SHA256 over the serialized payload
    computed_hmac = hmac.new(secret_bytes, serialized, hashlib.sha256).hexdigest()

    # 5. Perform a constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(computed_hmac, crypto_signature):
        return packet_info  # Signature verified
    else:
        return None          # Invalid signature

# Example usage (for testing purposes only):
if __name__ == "__main__":
    sample_packet = {"temperature": 23.5, "humidity": 45}
    # Precompute a valid signature for demonstration
    device_id = "device-001"
    secret_hex = TRUSTED_DEVICE_SIGNATURES[device_id]
    secret_bytes = bytes.fromhex(secret_hex)
    payload_bytes = json.dumps(sample_packet, separators=(",", ":"), sort_keys=True).encode("utf-8")
    valid_sig = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()

    result = verify_iot_signature(device_id, valid_sig, sample_packet)
    print("Verified:", result is not None)  # Should print True