import hashlib
import urllib.request
import urllib.error
from urllib.parse import urlparse

# Pre‑defined mapping of document URLs to their expected SHA256 signatures.
DOCUMENT_SIGNATURES = {
    # Example entries – replace with real data in production
    "https://example.com/doc1.pdf": "3b5d5c3712955042212316173ccf37be",
    "https://example.com/doc2.txt": "e5d8c9f3b7a6d4e1f2c0d12345678901",
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    location : str
        The URL of the document to verify.
    sign : str
        The cryptographic signature that should match the document.

    Returns
    -------
    bool
        ``True`` if the signature matches; otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Basic URL sanity check – only allow HTTP/HTTPS
    parsed = urlparse(location)
    if parsed.scheme not in ("http", "https"):
        raise IOError(f"Unsupported URL scheme: {parsed.scheme}")

    try:
        with urllib.request.urlopen(location) as resp:
            content = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document: {exc}") from exc

    # Compute the SHA256 hash of the retrieved content
    actual_hash = hashlib.sha256(content).hexdigest()

    # The expected signature is the hash stored in DOCUMENT_SIGNATURES
    expected_hash = DOCUMENT_SIGNATURES.get(location)

    # If no entry exists for the URL, treat as invalid
    if expected_hash is None:
        return False

    # Compare the provided signature with both the expected hash and the actual hash
    if sign.lower() != expected_hash.lower():
        return False

    # Ensure the content matches the stored hash (protection against tampering)
    return actual_hash.lower() == expected_hash.lower()