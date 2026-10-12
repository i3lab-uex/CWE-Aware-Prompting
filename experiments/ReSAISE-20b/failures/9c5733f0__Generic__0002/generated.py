import json
import hmac
import hashlib

# Global mapping of device IDs to their secret keys used for HMAC signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example: "device_123": b"my_secret_key",
}

def process_packet_data(id_device: str, packet_signature: str, packet_data: dict):
    """
    Authenticate and process data packets from IoT devices.

    Parameters
    ----------
    id_device : str
        Unique identifier of the sending device.
    packet_signature : str
        Hexadecimal HMAC‑SHA256 signature attached to the packet.
    packet_data : dict
        Payload of the packet.

    Returns
    -------
    dict or None
        The original `packet_data` if the signature is valid; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the device is unknown or a communication error occurs.
    """
    # 1. Verify that we have a trusted key for the device
    if id_device not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {id_device}")

    secret_key = TRUSTED_DEVICE_SIGNATURES[id_device]

    # 2. Prepare a canonical representation of the packet data
    try:
        serialized = json.dumps(packet_data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        # Malformed packet data; treat it as a communication error
        raise ConnectionError(f"Failed to serialize packet data: {exc}") from exc

    # 3. Compute the HMAC‑SHA256 signature
    computed_hmac = hmac.new(secret_key, serialized, hashlib.sha256).hexdigest()

    # 4. Compare the computed signature with the provided one in a timing‑safe manner
    if hmac.compare_digest(computed_hmac, packet_signature):
        # Signature is valid – return the original data
        return packet_data

    # Invalid signature: reject the packet
    return None