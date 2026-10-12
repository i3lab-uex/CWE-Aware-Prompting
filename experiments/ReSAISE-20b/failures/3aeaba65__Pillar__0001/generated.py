import hmac
import hashlib

# Global mapping of device IDs to their trusted signatures.
# In a real deployment this would be populated from a secure source
# (e.g., a database, an HSM, or a configuration file protected by ACLs).
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries:
    # "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    # "device_002": "e99a18c428cb38d5f260853678922e03",
}


def verify_iot_signature(iot_id: str, crypto_signature: str, packet_info: dict):
    """
    Validate the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    iot_id : str
        Unique identifier for the IoT device.
    crypto_signature : str
        Signature supplied by the device (hex encoded).
    packet_info : dict
        The payload of the data packet.

    Returns
    -------
    dict or None
        The original packet if signature verification succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If packet_info is missing or the device is not reachable.
    """
    # 1. Basic input validation
    if packet_info is None:
        raise ConnectionError("Failed to receive data from IoT device")

    # 2. Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if trusted_sig is None:
        # Device not registered or revoked
        return None

    # 3. Perform a constant‑time comparison to avoid timing attacks.
    # Convert both signatures to bytes for hmac.compare_digest.
    try:
        provided_bytes = bytes.fromhex(crypto_signature)
        trusted_bytes = bytes.fromhex(trusted_sig)
    except ValueError:
        # Malformed signature format
        return None

    if not hmac.compare_digest(provided_bytes, trusted_bytes):
        # Signature mismatch
        return None

    # 4. If we reach this point, the signature is valid.
    # Return a copy to prevent accidental mutation of the original packet.
    return dict(packet_info)