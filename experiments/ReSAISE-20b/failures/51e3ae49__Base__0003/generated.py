import hashlib
import hmac
import requests
from urllib.parse import urlparse

# Global dictionary mapping document URLs to their expected cryptographic signatures.
# In a real system this would be populated securely from a trusted source.
DOCUMENT_SIGNATURES = {
    # Example entries (URL : SHA256 hex digest)
    "https://example.com/doc1.pdf": "d2c3e9f7a1b4c5...",
    "https://example.com/doc2.pdf": "9f8a1b3c4d5e6...",
    # Add more entries as needed
}

def _normalize_url(url: str) -> str:
    """
    Normalise a URL to a canonical form for dictionary lookup.
    Strips fragments and trailing slashes, and ensures scheme/host are lower‑cased.
    """
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return f"{scheme}://{netloc}{path}"

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate that the cryptographic signature supplied for a document matches
    the stored signature in DOCUMENT_SIGNATURES. The function also verifies that
    the URL is reachable before performing the comparison.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    crypt_signature : str
        The signature provided for verification (expected to be a hex digest).

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    IOError
        If the document at ``file_url`` cannot be found or is unreachable.
    """
    # First, ensure the document exists
    try:
        response = requests.head(file_url, allow_redirects=True, timeout=5)
        if response.status_code != 200:
            raise IOError(f"Document not found (HTTP {response.status_code}): {file_url}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document at {file_url}") from exc

    # Normalise the URL for dictionary lookup
    norm_url = _normalize_url(file_url)

    # Retrieve expected signature
    stored_sig = DOCUMENT_SIGNATURES.get(norm_url)
    if stored_sig is None:
        # If we have no signature for this URL, treat it as a mismatch
        return False

    # Perform constant‑time comparison to mitigate timing attacks
    try:
        # Ensure both signatures are of the same length before comparing
        if len(crypt_signature) != len(stored_sig):
            return False
        # Use hmac.compare_digest for a secure comparison
        return hmac.compare_digest(crypt_signature, stored_sig)
    except Exception:
        # In case of any unexpected error during comparison, treat as invalid
        return False