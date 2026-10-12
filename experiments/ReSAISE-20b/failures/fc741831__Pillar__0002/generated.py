import hashlib
import hmac
from urllib.parse import urlparse

import requests


# Example dictionary mapping URLs to their expected SHA256 signatures.
# In a real application this would be populated with trusted values.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "3a7bd3e2360a...",
    # Add more URL:signature pairs as needed
}


def _compute_sha256(data: bytes) -> str:
    """Return the hex representation of the SHA‑256 hash of *data*."""
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()


def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its SHA‑256 hash
    against a known, trusted signature.

    Parameters
    ----------
    url : str
        The HTTPS URL of the document to be verified.
    crypt_signature : str
        The expected SHA‑256 hash (hex string) of the document.

    Returns
    -------
    bool
        ``True`` if the computed hash matches *crypt_signature*; otherwise
        ``False``.

    Raises
    ------
    IOError
        If the document cannot be retrieved from *url* or if the URL scheme is not HTTPS.
    """
    # Basic URL validation: only allow HTTPS to avoid man‑in‑the‑middle attacks
    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        raise IOError("Only HTTPS URLs are allowed for signature verification")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc

    # Compute the SHA‑256 hash of the retrieved content
    computed_hash = _compute_sha256(response.content)

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(computed_hash.lower(), crypt_signature.lower())