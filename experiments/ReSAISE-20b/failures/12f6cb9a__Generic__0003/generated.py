import requests
from urllib.parse import urlparse

# Global dictionary mapping document URLs to their expected signatures.
# Example:
# DOCUMENT_SIGNATURES = {
#     "https://example.com/docs/report.pdf": "abc123def456...",
# }
DOCUMENT_SIGNATURES = {}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the one stored
    for the document at `url`.

    Parameters
    ----------
    url : str
        The URL of the remote document to validate.
    doc_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the signatures match; False otherwise.

    Raises
    ------
    IOError
        If the document at `url` cannot be retrieved (e.g., 404 or network error).
    """
    # Normalise the URL so that different forms (with/without trailing slash,
    # http vs https) map to the same key in DOCUMENT_SIGNATURES.
    parsed = urlparse(url)
    norm_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    # Ensure the document exists on the remote server.
    try:
        resp = requests.get(norm_url, timeout=10)
        resp.raise_for_status()
    except requests.HTTPError as exc:
        # Raise IOError with a clear message for the caller.
        raise IOError(f"Document not found or inaccessible: {norm_url}") from exc
    except requests.RequestException as exc:
        raise IOError(f"Network error while accessing document: {norm_url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(norm_url)
    if expected_sig is None:
        # No stored signature for this document – treat as invalid.
        return False

    # Compare the provided signature with the stored one in a timing‑safe manner.
    return _timing_safe_compare(doc_signature, expected_sig)

def _timing_safe_compare(a: str, b: str) -> bool:
    """
    Compare two strings in a way that is resistant to timing attacks.
    Uses a constant‑time comparison algorithm.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0