import hashlib
import hmac
from urllib.parse import urlparse

import requests


# Pre‑defined dictionary mapping document URLs to their expected SHA‑256 hex digests
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "3a7bd3e2360a6b... (hex digest)",
    # ...
}


def _fetch_document(url: str) -> bytes:
    """
    Retrieve the raw content of a remote document.
    Raises IOError if the request fails or returns non‑2xx status code.
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.content
    except requests.RequestException as exc:
        raise IOError(f"Failed to retrieve document from {url!r}") from exc


def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate that the document at *location* matches the supplied cryptographic
    signature *sign* (expected to be a hex SHA‑256 digest).

    Parameters
    ----------
    location : str
        URL of the document to verify.
    sign : str
        Expected SHA‑256 hex digest for the document.

    Returns
    -------
    bool
        True if the signature matches, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from *location*.
    """
    # Normalise URL (basic validation)
    parsed = urlparse(location)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {location!r}")

    # Fetch the document content
    data = _fetch_document(location)

    # Compute SHA‑256 digest of the retrieved content
    computed_digest = hashlib.sha256(data).hexdigest()

    # Compare using constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(computed_digest, sign)