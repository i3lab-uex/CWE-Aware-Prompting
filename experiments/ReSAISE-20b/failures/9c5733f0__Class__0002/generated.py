import json
import hmac
import hashlib
import secrets

# Example trusted signatures dictionary.
# In a real system this would be securely loaded from a configuration store or
# key management service.  The value is the shared secret used to sign packets.
TRUSTED_DEVICE_SIGNATURES = {
    # "device_id": "hex-encoded-secret-key"
}

def process_packet_data(id_device: str, packet_signature: str, packet_data: dict) -> dict | None:
    """
    Validate the cryptographic signature of an IoT data packet and return the
    packet payload if it is authentic.

    Parameters
    ----------
    id_device : str
        Unique identifier for the IoT device sending the data.
    packet_signature : str
        Hex-encoded cryptographic signature attached to the packet.
    packet_data : dict
        The actual content of the data packet.

    Returns
    -------
    dict | None
        The original packet data if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or if there was an error during signature
        computation (e.g., corrupted packet, missing secret key).
    """
    # 1. Ensure the device is known
    try:
        secret_key_hex = TRUSTED_DEVICE_SIGNATURES[id_device]
    except KeyError as exc:
        raise ConnectionError(f"Unknown device or unreachable: {id_device}") from exc

    # 2. Convert secret key to bytes
    try:
        secret_key = bytes.fromhex(secret_key_hex)
    except ValueError as exc:
        raise ConnectionError("Invalid secret key format") from exc

    # 3. Serialize the packet data deterministically (sorted keys, no whitespace)
    try:
        serialized = json.dumps(packet_data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConnectionError("Failed to serialize packet data") from exc

    # 4. Compute the expected HMAC-SHA256 signature
    try:
        hmac_obj = hmac.new(secret_key, serialized, hashlib.sha256)
        expected_sig_hex = hmac_obj.hexdigest()
    except Exception as exc:
        raise ConnectionError("Failed to compute HMAC") from exc

    # 5. Perform constant‑time comparison to mitigate timing attacks
    if secrets.compare_digest(expected_sig_hex, packet_signature.lower()):
        return packet_data

    # Signature mismatch – data is not trusted
    return None