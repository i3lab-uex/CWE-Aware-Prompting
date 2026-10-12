import requests
from urllib.parse import urlparse, unquote
import hmac

# Global dictionary mapping normalized URLs to expected cryptographic signatures.
DOC_HASHES = {
    # Example entries:
    # "https://example.com/docs/report.pdf": "a1b2c3d4e5f6g7h8i9j0",
    # ...
}

def _normalize_url(url: str) -> str:
    """
    Normalise a URL for use as a key in DOC_HASHES.
    This removes the scheme and trailing slashes, and decodes percent-encoding.
    """
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = unquote(parsed.path).rstrip('/')
    return f"https://{netloc}{path}"

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a document located at ``resource_url``.
    
    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        ``True`` if the signature matches, ``False`` otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible.
    """
    # Ensure we can reach the resource; do not rely on its content for verification.
    try:
        resp = requests.head(resource_url, timeout=5)
        if resp.status_code >= 400:
            raise IOError(f"Document not accessible: HTTP {resp.status_code}")
    except (requests.RequestException, requests.ConnectionError) as exc:
        raise IOError(f"Unable to reach document: {exc}") from exc

    # Determine the expected signature.
    key = _normalize_url(resource_url)
    expected_sig = DOC_HASHES.get(key)

    if expected_sig is None:
        # No known signature for this document; treat as invalid.
        return False

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(crypto_signature, expected_sig)