# process_packet_data.py

"""
Implementation of `process_packet_data` for authenticating IoT data packets.

Security considerations:
- Uses constant‑time comparison (`hmac.compare_digest`) to prevent timing attacks.
- Raises `ConnectionError` if data cannot be received (simulated by a flag).
- Returns the packet payload only when its signature matches the trusted
  signature stored in `TRUSTED_DEVICE_SIGNATURES`.

CWE-345: Insufficient Verification of Data Authenticity is mitigated by
verifying the signature against a trusted source before processing.
"""

import hmac
from typing import Dict, Optional

# Global mapping of device ID to its trusted signature.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "device_A": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_B": "e99a18c428cb38d5f260853678922e03",
    # Add more device signatures as needed.
}


def process_packet_data(
    id_device: str, packet_signature: str, packet_data: Dict
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    id_device : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Cryptographic signature included with the data packet.
    packet_data : dict
        The actual payload of the packet.

    Returns
    -------
    dict | None
        The packet data if authentication succeeds, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet could not be received (simulated condition).
    """
    # Simulate a scenario where data reception fails.
    if packet_data is None:
        raise ConnectionError("Failed to receive data from device: " + id_device)

    # Retrieve the trusted signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if not expected_sig:
        # Unknown device – treat as unauthenticated.
        return None

    # Constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(packet_signature, expected_sig):
        # Signature mismatch – do not trust the data.
        return None

    # All checks passed; return the packet payload.
    return packet_data