import hashlib
import hmac
from typing import Dict

import requests


# Pre‑defined dictionary mapping document URLs to their authentic SHA256 signatures.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries (URL : SHA256 signature)
    "https://example.com/doc1.pdf": "3a7bd3e2360a6f5c4b8d2d1f6f9c3e7b0a1c2d4e5f67890123456789abcdef12",
    "https://example.com/doc2.pdf": "6b9c8a5f1d3e7c4b2a0f9e8d6c5b4a3d1f7e2c9b0a8d7c6e5f4d3b2a1c0e9f8",
    # Add more entries as needed
}


def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document by comparing its
    SHA256 signature with an expected value.

    Parameters
    ----------
    document_location : str
        URL of the document to be validated.
    crypto_sign : str
        The cryptographic signature (hex digest) provided for validation.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Ensure the document is known
    expected_signature = DOCUMENT_SIGNATURES.get(document_location)
    if not expected_signature:
        # Unknown document – cannot verify
        return False

    try:
        response = requests.get(document_location, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Failed to retrieve document from {document_location}") from exc

    # Compute SHA256 of the downloaded content
    sha256 = hashlib.sha256()
    sha256.update(response.content)
    computed_signature = sha256.hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_signature, expected_signature):
        return False

    # Additionally ensure the provided crypto_sign matches the computed one
    if not hmac.compare_digest(computed_signature, crypto_sign):
        return False

    return True