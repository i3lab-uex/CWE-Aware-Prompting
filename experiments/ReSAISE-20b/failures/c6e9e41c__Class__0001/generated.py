import hmac
from typing import Dict, Optional

# Global dictionary that maps each device ID to its trusted cryptographic signature.
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – in a real system these would be securely stored and
    # never hard‑coded. They should be byte strings (e.g., SHA‑256 digests).
    "device_a": b"\x01\x23\x45\x67\x89\xab\xcd\xef",
    "device_b": b"\xfe\xdc\xba\x98\x76\x54\x32\x10",
    # Add more device signatures here
}


def verify_data_packet(device: str, sig: str, payload: Dict) -> Optional[Dict]:
    """
    Validate an incoming data packet from an IoT device.

    Parameters
    ----------
    device : str
        The unique identifier of the IoT device that sent the packet.
    sig : str
        The cryptographic signature attached to the packet. It is expected
        to be a hex string representation of the raw bytes.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is verified successfully;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be processed due to missing device information,
        malformed signature, or other I/O issues.
    """
    # Ensure the packet contains a payload; if not, treat it as a communication issue.
    if payload is None or not isinstance(payload, dict):
        raise ConnectionError("Malformed packet: payload missing or invalid.")

    # Check that the device is known and has a trusted signature.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device)
    if expected_sig is None:
        raise ConnectionError(f"Unknown device: {device}")

    # Convert the provided signature from hex string to bytes.
    try:
        sig_bytes = bytes.fromhex(sig)
    except ValueError as exc:
        raise ConnectionError("Invalid signature format.") from exc

    # Perform a constant‑time comparison to prevent timing attacks.
    if hmac.compare_digest(sig_bytes, expected_sig):
        return payload

    # Signature verification failed – do not trust the data.
    return None