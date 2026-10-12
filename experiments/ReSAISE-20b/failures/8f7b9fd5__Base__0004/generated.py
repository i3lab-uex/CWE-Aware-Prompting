import hmac
import hashlib
import json
from typing import Dict, Any, Optional

# Global mapping of device_id -> pre‑shared secret key (hex string)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real secrets
    "device_001": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
    "device_002": "1a2b3c4d5e6f708192a3b4c5d6e7f8a9",
    # ...
}


def _compute_hmac(message: bytes, key_hex: str) -> bytes:
    """
    Compute HMAC-SHA256 of the given message using the provided hex key.
    """
    key = bytes.fromhex(key_hex)
    return hmac.new(key, message, hashlib.sha256).digest()


def _constant_time_compare(a: bytes, b: bytes) -> bool:
    """
    Constant‑time comparison to mitigate timing attacks.
    """
    return hmac.compare_digest(a, b)


def process_packet(device_id: str,
                   packet_signature: str,
                   data_packet: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validate the cryptographic signature of an IoT data packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Hex‑encoded cryptographic signature that accompanies the packet.
    data_packet : dict
        The payload of the packet to be processed.

    Returns
    -------
    dict or None
        The processed data if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., ``data_packet`` is missing).
    """
    # 1. Ensure the packet was received
    if data_packet is None:
        raise ConnectionError("Data packet could not be received.")

    # 2. Verify that the device is trusted
    secret_key_hex = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not secret_key_hex:
        # Unknown device – reject without processing
        return None

    # 3. Canonicalise the data packet (stable JSON representation)
    try:
        payload_bytes = json.dumps(
            data_packet,
            separators=(",", ":"),
            sort_keys=True
        ).encode("utf-8")
    except (TypeError, ValueError):
        # Payload cannot be serialised – treat as invalid
        return None

    # 4. Compute expected HMAC
    expected_hmac = _compute_hmac(payload_bytes, secret_key_hex)

    # 5. Decode the provided signature (hex -> bytes)
    try:
        received_hmac = bytes.fromhex(packet_signature)
    except ValueError:
        # Signature is not valid hex
        return None

    # 6. Constant‑time comparison to avoid timing attacks
    if not _constant_time_compare(expected_hmac, received_hmac):
        return None

    # 7. Signature is valid – process the packet (example: just return it)
    # In a real system, additional validation or transformation would occur here.
    return data_packet