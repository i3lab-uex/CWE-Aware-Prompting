import hmac
import hashlib
import random

# Example global dictionary mapping device IDs to their trusted HMAC secret keys.
TRUSTED_DEVICE_SIGNATURES = {
    "device_A": b"super_secret_key_for_device_A",
    "device_B": b"another_very_secret_key",
    # Add more devices as needed.
}

def _simulate_packet_loss() -> None:
    """
    Randomly simulates a packet loss scenario.
    Raises ConnectionError with a low probability to mimic real-world unreliability.
    """
    if random.random() < 0.01:  # 1% chance of packet loss
        raise ConnectionError("Failed to receive the IoT packet.")


def _validate_signature(device_id: str, crypt_sig: str, pkt_data: dict) -> bool:
    """
    Validates the provided cryptographic signature against a HMAC-SHA256
    computed from the packet data using the device's trusted secret key.

    Args:
        device_id: Identifier of the sending device.
        crypt_sig: Hex-encoded HMAC signature received with the packet.
        pkt_data: The payload dictionary to be validated.

    Returns:
        True if signatures match; False otherwise.
    """
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not secret_key:
        # Unknown device – treat as invalid.
        return False

    # Canonicalize the packet data to a deterministic byte representation.
    # Here we sort keys and encode as UTF-8 JSON for reproducibility.
    import json
    pkt_bytes = json.dumps(pkt_data, sort_keys=True).encode("utf-8")

    # Compute HMAC-SHA256 of the packet bytes.
    computed_hmac = hmac.new(secret_key, pkt_bytes, hashlib.sha256).hexdigest()

    # Use constant-time comparison to mitigate timing attacks.
    return hmac.compare_digest(computed_hmac, crypt_sig)


def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: dict) -> dict | None:
    """
    Validates and processes an IoT packet.

    The function first simulates the possibility of a lost packet. If the
    packet is received, it verifies the cryptographic signature using HMAC.
    When validation succeeds, the packet data is returned unchanged; otherwise
    None is returned.

    Args:
        device_id: Unique identifier for the IoT device.
        crypt_sig: Cryptographic signature sent with the packet (hex string).
        pkt_data: The content of the data packet.

    Returns:
        dict: Processed packet data if validation succeeds.
        None: If signature validation fails.

    Raises:
        ConnectionError: If the packet cannot be received due to simulated loss.
    """
    # Simulate a possible connection failure.
    _simulate_packet_loss()

    if not _validate_signature(device_id, crypt_sig, pkt_data):
        # Signature mismatch – drop the packet.
        return None

    # Here we would normally perform further processing (e.g., storing data,
    # triggering actions, etc.). For this example we simply return the packet.
    return pkt_data