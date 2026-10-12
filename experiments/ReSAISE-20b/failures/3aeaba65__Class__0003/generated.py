import hmac
import hashlib

# Global mapping of device IDs to their expected HMAC keys or signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries (replace with real values in production)
    "device-001": b"supersecretkey1",
    "device-002": b"supersecretkey2",
}

def verify_iot_signature(iot_id: str, crypto_signature: str, packet_info: dict):
    """
    Validate the cryptographic signature of an IoT data packet and return
    the packet content if valid.

    Parameters:
        iot_id (str): Unique identifier of the IoT device.
        crypto_signature (str): Hex-encoded signature sent with the packet.
        packet_info (dict): The actual data payload.

    Returns:
        dict: The original packet content if the signature is verified.
        None: If verification fails.

    Raises:
        ConnectionError: If there is an issue retrieving the packet or its signature.
    """
    # 1. Ensure we have a trusted key for this device
    try:
        key = TRUSTED_DEVICE_SIGNATURES[iot_id]
    except KeyError as exc:
        # No trusted key found for this device – treat as a connection problem
        raise ConnectionError(f"Untrusted device ID: {iot_id}") from exc

    # 2. Recreate the expected signature
    try:
        # Convert packet_info to a canonical string representation.
        # Using JSON ensures consistent ordering of keys.
        import json
        packet_bytes = json.dumps(packet_info, sort_keys=True).encode("utf-8")
    except Exception as exc:
        # If we cannot serialize the packet, treat it as a data reception issue.
        raise ConnectionError("Failed to process packet payload") from exc

    # 3. Compute HMAC-SHA256 over the packet bytes
    hmac_obj = hmac.new(key, msg=packet_bytes, digestmod=hashlib.sha256)
    expected_signature = hmac_obj.hexdigest()

    # 4. Compare signatures using constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(expected_signature, crypto_signature.lower()):
        # Signature mismatch – reject the packet
        return None

    # 5. All checks passed – return the original payload
    return packet_info