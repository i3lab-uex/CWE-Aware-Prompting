import hashlib
import requests
from urllib.parse import urlparse

# Example signature store (key: URL, value: expected SHA-256 hex digest)
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    # Add real entries here
}

def _compute_sha256(content: bytes) -> str:
    """Return the SHA‑256 hex digest of given binary content."""
    return hashlib.sha256(content).hexdigest()

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate that the remote document at *url* matches the supplied cryptographic
    signature.

    Parameters
    ----------
    url : str
        The URL of the remote document.
    crypt_signature : str
        Expected SHA‑256 hex digest for the document.

    Returns
    -------
    bool
        ``True`` if the signature matches, ``False`` otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from *url*.
    """
    # Normalise URL to ensure consistent dictionary lookup
    parsed = urlparse(url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc

    content = resp.content
    computed_sig = _compute_sha256(content)

    # Compare the supplied signature with both the provided crypt_signature
    # and the expected value from DOCUMENT_SIGNATURES (if present).
    if computed_sig != crypt_signature:
        return False

    expected = DOCUMENT_SIGNATURES.get(normalized_url)
    if expected is not None and computed_sig != expected:
        return False

    return True