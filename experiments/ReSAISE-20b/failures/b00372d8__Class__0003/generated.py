import hmac
import hashlib

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries; in practice these would be securely stored.
    "device_001": b"\x01\x23\x45\x67",
    "device_002": b"\xab\xcd\xef\x01",
}

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: dict) -> dict | None:
    """
    Validate the cryptographic signature of an IoT packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device.
    crypt_sig : str
        Hex-encoded signature provided with the packet.
    pkt_data : dict
        Payload of the packet.

    Returns
    -------
    dict | None
        The processed data if validation succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received or the device is unknown.
    """
    # Validate input types
    if not isinstance(device_id, str):
        raise TypeError("device_id must be a string")
    if not isinstance(crypt_sig, str):
        raise TypeError("crypt_sig must be a string")
    if not isinstance(pkt_data, dict):
        raise TypeError("pkt_data must be a dictionary")

    # Ensure we have received data
    if not pkt_data:
        raise ConnectionError("Packet data is empty or missing")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        raise ConnectionError(f"Unknown device ID: {device_id}")

    # Convert the provided signature from hex to bytes
    try:
        provided_sig = bytes.fromhex(crypt_sig)
    except ValueError as exc:
        raise ValueError("Provided signature is not valid hex") from exc

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(provided_sig, expected_sig):
        # Signature mismatch – reject the packet
        return None

    # At this point, the signature is verified.
    # Here we simply return a copy of pkt_data as "processed" data.
    processed = dict(pkt_data)  # shallow copy; adjust as needed for real processing
    return processed