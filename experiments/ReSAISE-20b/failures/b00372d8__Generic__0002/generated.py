import hmac
import hashlib

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries – replace with actual device IDs and signatures.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0123456789abcdef1234",
}


def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: dict) -> dict | None:
    """
    Validate a packet from an IoT device and return the processed data.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Cryptographic signature accompanying the packet.
    pkt_data : dict
        Payload of the data packet.

    Returns
    -------
    dict | None
        The processed data dictionary if validation succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet could not be received (e.g., pkt_data is None).
    """

    # 1. Ensure packet was received
    if pkt_data is None:
        raise ConnectionError(f"Packet from device {device_id} could not be received.")

    # 2. Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Device not known – treat as unauthenticated
        return None

    # 3. Securely compare the provided signature with the expected one.
    #    Use hmac.compare_digest to avoid timing attacks.
    if not hmac.compare_digest(crypt_sig, expected_sig):
        # Signature mismatch – reject the packet
        return None

    # 4. Process the data packet.
    #    For this example, we simply return the payload unchanged,
    #    but real processing logic would go here.
    processed_data = pkt_data.copy()
    processed_data["device_id"] = device_id
    processed_data["validated_at"] = __import__("time").time()

    return processed_data