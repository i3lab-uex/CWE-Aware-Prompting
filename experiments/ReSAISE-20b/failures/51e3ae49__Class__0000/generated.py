import hashlib
import hmac
from urllib.parse import urlparse

import requests

# Example global dictionary of correct signatures for known documents.
# In a real system this would be securely stored and protected.
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': 'sha256:abcd1234...',
    # Add entries as needed
}


def _fetch_document_head(url: str) -> requests.Response:
    """
    Perform a HEAD request to ensure the document exists.
    Raises IOError if the status code is not 200.
    """
    try:
        resp = requests.head(url, timeout=10)
        resp.raise_for_status()
        return resp
    except requests.HTTPError as exc:
        if exc.response.status_code == 404:
            raise IOError(f"Document not found at {url}") from exc
        raise


def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the
    expected signature for a document located at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    crypt_signature : str
        The signature supplied for verification.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` cannot be retrieved (404 or other error).
    """
    # Ensure the document exists
    _fetch_document_head(file_url)

    # Normalize URL for dictionary lookup (strip fragment and query)
    parsed = urlparse(file_url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    # Retrieve the expected signature
    expected_sig = DOCUMENT_SIGNATURES.get(normalized_url)
    if expected_sig is None:
        # If we don't have a stored signature, treat it as invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(crypt_signature, expected_sig)