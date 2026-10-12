import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected signatures.
# In a real deployment this would be securely stored and protected
# (e.g., in an HSM or a secure vault). Here it is simply defined for
# demonstration purposes.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device-001": "a3f1c2d4e5b6",
    "device-002": "7e8f9a0b1c2d",
    # ... add more trusted device signatures
}

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate an IoT device data packet and return the processed data.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the IoT device sending the packet.
    iot_signature : str
        Cryptographic signature sent along with the packet.
    iot_data : dict or None
        The content of the data packet to be processed.

    Returns
    -------
    dict or None
        The original `iot_data` dictionary if the signature validation
        succeeds; otherwise, `None`.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (i.e., `iot_data` is None).
    """
    # Step 1: Ensure the packet was received successfully.
    if iot_data is None:
        raise ConnectionError("Failed to receive data packet from device.")

    # Step 2: Retrieve the expected signature for this device.
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if expected_signature is None:
        # Device not recognized; reject the packet.
        return None

    # Step 3: Perform a constant‑time comparison to mitigate timing attacks.
    # The `compare_digest` function is resistant to subtle timing leaks.
    if not hmac.compare_digest(iot_signature, expected_signature):
        # Signature mismatch; reject the packet.
        return None

    # Step 4: All checks passed – process (here we simply return the data).
    return iot_data