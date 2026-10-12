import hmac
import hashlib

# Example trusted signatures dictionary (device_id -> secret key)
TRUSTED_DEVICE_SIGNATURES = {
    # device_id: secret_key (bytes)
    "device_001": b"supersecretkey1",
    "device_002": b"anothersecret2",
    # Add more device entries as needed
}


def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: dict):
    """
    Authenticate and process an IoT data packet.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the sending IoT device.
    crypto_sign : str
        Hex‑encoded HMAC SHA256 signature attached to the packet.
    packet_content : dict
        The actual data payload of the packet.

    Returns
    -------
    dict or None
        Returns the packet content if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If packet_content cannot be received (e.g., None or empty).
    ValueError
        If dev_id is not registered.
    """
    # 1. Validate that we received a packet
    if packet_content is None:
        raise ConnectionError("Failed to receive data from IoT device.")

    # 2. Ensure the device is known
    if dev_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ValueError(f"Unknown device ID: {dev_id}")

    # 3. Compute the expected HMAC over the packet content
    secret_key = TRUSTED_DEVICE_SIGNATURES[dev_id]
    # Convert the packet content to a canonical byte representation
    # For deterministic ordering, serialize with sorted keys.
    import json
    packet_bytes = json.dumps(packet_content, sort_keys=True).encode("utf-8")

    expected_hmac = hmac.new(secret_key, packet_bytes, hashlib.sha256).hexdigest()

    # 4. Compare signatures securely to avoid timing attacks
    if not hmac.compare_digest(expected_hmac, crypto_sign):
        # Signature mismatch – treat as invalid packet
        return None

    # 5. Return the payload as trusted data
    return packet_content