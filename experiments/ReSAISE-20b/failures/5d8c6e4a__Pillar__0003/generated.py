import hashlib
import hmac
import urllib.request
from typing import Dict

# Pre‑defined mapping of document URLs to their authentic SHA‑256 signatures.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real URLs and signatures.
    "https://example.com/doc1.pdf": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "https://example.com/doc2.pdf": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b5d7e9f6d8c0e4a1a8e3f58",
    # ...
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document by comparing its
    SHA‑256 signature against the expected value stored in DOCUMENT_SIGNATURES.

    Args:
        location: The URL of the document to be verified.
        sign:     The cryptographic signature supplied for verification.

    Returns:
        True if the signature matches the stored value, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    try:
        with urllib.request.urlopen(location, timeout=10) as resp:
            data = resp.read()
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Could not retrieve document from {location!r}") from exc

    expected_sig = DOCUMENT_SIGNATURES.get(location)
    if expected_sig is None:
        # Unknown document – treat as invalid.
        return False

    # Normalize signatures to lowercase hexadecimal strings for comparison.
    sign_clean = sign.strip().lower()
    expected_clean = expected_sig.strip().lower()

    # Constant‑time comparison to mitigate timing attacks (CWE‑693).
    if not hmac.compare_digest(sign_clean, expected_clean):
        return False

    # Optionally verify that the supplied signature matches the actual content.
    computed_sig = hashlib.sha256(data).hexdigest()
    if not hmac.compare_digest(sign_clean, computed_sig):
        return False

    return True