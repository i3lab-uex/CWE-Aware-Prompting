import json
import hmac
import hashlib
from typing import Dict, Any

# Example trusted signatures mapping.
# In a real system these would be securely stored and retrieved,
# e.g. from a vault or database.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # device_id : secret key (hex-encoded)
    "device_001": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef",
    "device_002": "f0e1d2c3b4a5968778899aabbccddeeff00112233445566778899aabbccddeee",
    # Add more devices as needed
}


def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Validate the cryptographic signature of an IoT data packet and process it.

    Args:
        device_id: Unique identifier for the sending IoT device.
        crypt_sig: Hex-encoded signature provided with the packet.
        pkt_data: Dictionary containing the payload of the data packet.

    Returns:
        The processed data dictionary if the signature is valid; otherwise, None.

    Raises:
        ConnectionError: If the packet cannot be received successfully
                         (e.g., missing data or unknown device).
    """
    # Basic sanity checks – in a real system these might be more elaborate.
    if pkt_data is None:
        raise ConnectionError("Packet data missing or unreadable")

    # Retrieve the secret key for this device.
    try:
        secret_hex = TRUSTED_DEVICE_SIGNATURES[device_id]
    except KeyError as exc:
        raise ConnectionError(f"Unknown device ID: {device_id}") from exc

    # Convert the hex-encoded secret to bytes.
    try:
        secret = bytes.fromhex(secret_hex)
    except ValueError as exc:
        raise ConnectionError(f"Invalid secret format for device {device_id}") from exc

    # Serialize the packet data deterministically.
    try:
        payload = json.dumps(pkt_data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConnectionError("Failed to serialize packet data") from exc

    # Compute HMAC-SHA256 over the payload.
    computed_hmac = hmac.new(secret, payload, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to prevent timing attacks.
    if not hmac.compare_digest(computed_hmac, crypt_sig.lower()):
        # Signature mismatch – do not process the packet.
        return None

    # At this point the signature is verified; perform any desired processing.
    # For demonstration, we simply return the original data unchanged.
    return pkt_data