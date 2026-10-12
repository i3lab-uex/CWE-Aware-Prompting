import hmac
import hashlib
from typing import Dict, Any

# Global mapping of device IDs to their shared secret keys (used for HMAC signatures)
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    "device_a": b"secret_key_1",
    "device_b": b"another_secret_2",
    # Add more trusted devices here
}


def process_packet_data(
    id_device: str, packet_signature: str, packet_data: Dict[str, Any]
) -> Dict[str, Any] | None:
    """
    Authenticate an IoT data packet using HMAC and return the packet content if valid.

    Parameters
    ----------
    id_device : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Hexadecimal HMAC-SHA256 signature of the JSON-encoded packet data.
    packet_data : dict
        The actual payload of the data packet.

    Returns
    -------
    dict | None
        The original packet data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is not in the trusted list or if packet reception fails.
    """
    # 1. Verify that we have a key for this device
    secret = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if secret is None:
        raise ConnectionError(f"Untrusted device ID: {id_device}")

    # 2. Recompute the HMAC of the packet data
    try:
        # Convert packet_data to a canonical byte representation (JSON with sorted keys)
        import json

        payload_bytes = json.dumps(packet_data, sort_keys=True).encode("utf-8")
    except Exception as exc:
        # Any serialization error is treated as a data‑corruption issue
        raise ConnectionError(f"Failed to serialize packet data: {exc}") from exc

    computed_hmac = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()

    # 3. Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(computed_hmac, packet_signature):
        # Signature mismatch – data is untrusted
        return None

    # 4. All checks passed; return the packet data
    return packet_data


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Simulate a packet from device_a
    test_data = {"temperature": 22.5, "humidity": 45}
    secret_key = TRUSTED_DEVICE_SIGNATURES["device_a"]
    payload_bytes = json.dumps(test_data, sort_keys=True).encode("utf-8")
    signature_hex = hmac.new(secret_key, payload_bytes, hashlib.sha256).hexdigest()

    result = process_packet_data("device_a", signature_hex, test_data)
    print(result)  # Should output the original dictionary