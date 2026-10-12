import hmac

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries; populate with real values in production
    "device_a": "sha256$abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx",
    "device_b": "sha256$1234abcd5678efgh9012ijkl3456mnop7890qrstuvwx",
    # Add more devices as needed
}


def verify_data_packet(device: str, sig: str, payload: dict) -> dict | None:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the sending device.
    sig : str
        Cryptographic signature attached to the packet.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        Returns the payload dictionary if signature verification succeeds,
        otherwise returns ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown, the payload is not a dictionary,
        or any network-related error occurs while receiving the packet.
    """
    # Basic sanity checks
    if not isinstance(device, str):
        raise ConnectionError("Device identifier must be a string.")
    if not isinstance(sig, str):
        raise ConnectionError("Signature must be a string.")
    if not isinstance(payload, dict):
        raise ConnectionError("Payload must be a dictionary.")

    # Ensure the device is known
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device)
    if trusted_sig is None:
        raise ConnectionError(f"Unknown device: {device}")

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig, trusted_sig):
        # Signature does not match; reject the packet
        return None

    # If we reach here, the signature is verified
    return payload