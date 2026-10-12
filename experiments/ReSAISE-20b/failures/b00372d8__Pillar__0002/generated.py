import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their known cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – in a real system these would be securely stored.
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "deadbeefcafebabe1234",
}

def process_iot_packet(
    device_id: str,
    crypt_sig: str,
    pkt_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Cryptographic signature provided with the packet.
    pkt_data : dict | None
        The payload of the packet.

    Returns
    -------
    dict | None
        The processed data if signature verification succeeds; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet could not be received (e.g., ``pkt_data`` is None).
    """
    # 1. Ensure we actually received a packet.
    if pkt_data is None:
        raise ConnectionError(f"Packet from device '{device_id}' could not be received.")

    # 2. Fetch the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Device not recognized – reject the packet.
        return None

    # 3. Perform a constant‑time comparison to avoid timing attacks
    # (CWE‑693: protection mechanism failure).
    if not hmac.compare_digest(expected_sig, crypt_sig):
        # Signature mismatch – reject the packet.
        return None

    # 4. At this point, signature is verified – process the packet.
    # In a real implementation, additional validation or transformation would occur here.
    processed = dict(pkt_data)  # shallow copy to avoid mutating the caller's data
    processed["validated_by"] = device_id

    return processed