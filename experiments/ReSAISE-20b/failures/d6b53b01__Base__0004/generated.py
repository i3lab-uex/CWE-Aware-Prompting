import hashlib
import hmac
from typing import Dict

import requests


# Pre‑defined mapping of document URLs to their authentic SHA256 signatures
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real URLs and signatures)
    "https://example.com/doc1.pdf": "3a7bd3e2360a4c5b9f2d8e6f1c7ab3d0e4f12a5b9f2c8d6e1a7c3b9d0e4f12a5",
    "https://example.com/doc2.pdf": "1b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3",
    # Add more documents as required
}


def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate that the document at ``document_location`` matches its expected
    cryptographic signature.

    Parameters
    ----------
    document_location : str
        The URL of the remote document to validate.
    crypto_sign : str
        The signature supplied for verification. It should be a hex string
        representing the SHA256 digest of the document content.

    Returns
    -------
    bool
        ``True`` if the retrieved document matches its stored signature,
        otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    try:
        response = requests.get(document_location, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Any problem retrieving the file is treated as an IO error
        raise IOError(f"Unable to retrieve document from {document_location}") from exc

    # Compute SHA256 hash of the content
    computed_hash = hashlib.sha256(response.content).hexdigest()

    # Retrieve expected signature from the authoritative source
    expected_hash = DOCUMENT_SIGNATURES.get(document_location)

    # If no stored signature exists, we cannot validate; treat as failure
    if expected_hash is None:
        return False

    # Use constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(computed_hash, expected_hash) and \
       hmac.compare_digest(crypto_sign.lower(), expected_hash.lower()):
        return True

    return False