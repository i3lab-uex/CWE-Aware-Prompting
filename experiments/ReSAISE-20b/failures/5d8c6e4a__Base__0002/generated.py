import hashlib
import hmac
import urllib.request
from typing import Dict

# Pre‑defined dictionary containing the authentic SHA‑256 signatures of remote documents.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries (URL : SHA-256 hex digest of the file contents)
    "https://example.com/file1.pdf": "d2c7f0b8e5a4d3b6e9f1c2a3b4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3",
    "https://example.com/file2.txt": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
    # Add more entries as needed.
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its computed SHA‑256
    signature against the expected signature.

    Parameters:
        location (str): URL of the document to be verified.
        sign (str): The cryptographic signature provided for verification.

    Returns:
        bool: True if the computed signature matches the provided one, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    try:
        with urllib.request.urlopen(location, timeout=10) as resp:
            content = resp.read()
    except Exception as exc:          # pragma: no cover
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # Compute SHA‑256 digest of the retrieved content
    computed_hash = hashlib.sha256(content).hexdigest()

    # Verify that the provided signature matches both the stored and computed signatures
    expected_hash = DOCUMENT_SIGNATURES.get(location)
    if expected_hash is None:
        # No stored signature for this URL – treat as invalid
        return False

    # Constant‑time comparison to mitigate timing attacks (CWE-347)
    if not hmac.compare_digest(computed_hash, expected_hash):
        return False
    if not hmac.compare_digest(computed_hash, sign):
        return False

    return True