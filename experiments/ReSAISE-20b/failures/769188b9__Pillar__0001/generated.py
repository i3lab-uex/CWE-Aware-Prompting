import requests
from hmac import compare_digest
from typing import Dict

# Global dictionary mapping resource URLs to their expected cryptographic signatures.
DOC_HASHES: Dict[str, str] = {
    # Example entries; in practice these would be populated securely.
    "https://example.com/doc1.pdf": "a3f5c2e9b7d4...",
    "https://example.com/doc2.pdf": "5d1e6f8a9c0b...",
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that a document's cryptographic signature matches the expected value.

    Parameters
    ----------
    resource_url : str
        URL of the document to validate.
    crypto_signature : str
        Cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` cannot be accessed.
    """
    # First, confirm that the resource is reachable to guard against
    # potential denial‑of‑service or man‑in‑the‑middle attacks.
    try:
        # Use a lightweight HEAD request; fallback to GET if unsupported.
        response = requests.head(resource_url, timeout=5)
        if response.status_code >= 400:
            # Some servers may not support HEAD; try GET for existence.
            response = requests.get(resource_url, stream=True, timeout=5)
            if response.status_code >= 400:
                raise IOError(f"Unable to access document: HTTP {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document: {exc}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # No known signature; treat as invalid.
        return False

    # Use a constant‑time comparison to avoid timing attacks (CWE‑693).
    return compare_digest(crypto_signature, expected_sig)