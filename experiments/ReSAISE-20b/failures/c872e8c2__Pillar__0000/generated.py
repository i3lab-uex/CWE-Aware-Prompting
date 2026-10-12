import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
# In a real deployment this would be stored securely, e.g., in a hardware
# security module or encrypted configuration file.
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries; replace with actual device IDs and signatures.
    "device_001": b"\x01\x23\x45\x67\x89\xab\xcd\xef",
    "device_002": b"\xfe\xdc\xba\x98\x76\x54\x32\x10",
}


def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict,
) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        The unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        The cryptographic signature attached to the packet. Expected to be a
        hexadecimal string.
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        Returns the packet data if the signature is verified; otherwise,
        returns ``None``.

    Raises
    ------
    ConnectionError
        If the packet could not be received (e.g., missing parameters).
    """
    # Validate input presence
    if io_device_id is None or crypto_signature is None or packet_data is None:
        raise ConnectionError("Incomplete data packet received from device.")

    # Retrieve the trusted signature for this device
    trusted_sig_bytes = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if trusted_sig_bytes is None:
        # Unknown device – treat as a potential security threat
        return None

    try:
        # Convert the provided signature from hex string to bytes
        provided_sig_bytes = bytes.fromhex(crypto_signature)
    except ValueError:
        # Malformed signature string
        return None

    # Perform a constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(provided_sig_bytes, trusted_sig_bytes):
        # Signature mismatch – do not trust the payload
        return None

    # If we reach this point, the signature is valid.
    # Further processing of packet_data can be performed here if needed.
    return packet_data